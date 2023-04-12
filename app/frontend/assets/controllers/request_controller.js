import { Controller } from '@hotwired/stimulus';

let specifiek_graf = 1
let form = null
let inputList = null
let checkboxList = null
let formData = null
const defaultErrorMessage = "Vul a.u.b. dit veld in."
export default class extends Controller {

    static targets = ["aannemerField", "specifiekGrafField"]
    static values = {
        medewerkers: String,
        categorie_andere_oorzaak: String,
        specifiek_graf_categorieen: String
    }

    connect() {
        console.log('request_controller conected')
        this.aannemerFieldTarget.setAttribute("disabled", "disabled")

        form = document.querySelector("form");
        inputList = document.querySelectorAll('[type="text"], [type="radio"], select, textarea')
        checkboxList = document.querySelectorAll('[type="checkbox"]')

        formData = new FormData(form)

        //check radiobutton
        document.getElementById('id_specifiek_graf_0').click()

        for (let i=0; i<inputList.length; i++){
            const input = inputList[i]
            const error = input.closest('.form-row').getElementsByClassName('invalid-text')[0]

            input.addEventListener("input", (event) => {
                if (input.validity.valid) {
                    input.closest('.form-row').classList.remove('is-invalid')
                    error.textContent = "";
                } else {
                    error.textContent = defaultErrorMessage;
                    input.closest('.form-row').classList.add('is-invalid')
                }
            })
        };

        for (let i=0; i<checkboxList.length; i++){
            const cb = checkboxList[i]

            cb.addEventListener("input", () => {
                this.checkCheckBoxes()
            })
        };

        form.addEventListener("submit", (event) => {

            const allFieldsValid = this.checkValids()
            const checkBoxesValid = this.checkCheckBoxes()

            if(!(checkBoxesValid && allFieldsValid)){
                const errorList = document.querySelectorAll('div.is-invalid')
                errorList[0].scrollIntoView({ behavior: "smooth"})
                event.preventDefault();
            }
        });
    }

    checkValids() {
        //check all inputfields (except checkboxes) for validity
        // if 1 or more fields is invalid, don't send the form (return false)
        inputList = document.querySelectorAll('[type="text"], [type="radio"], select, textarea')
        let count = 0
        for (let i=0; i<inputList.length; i++){
            const input = inputList[i]
            const error = input.closest('.form-row').getElementsByClassName('invalid-text')[0]
            if (input.validity.valid) {
                error.textContent = "";
                input.closest('.form-row').classList.remove('is-invalid')
            } else {
                error.textContent = defaultErrorMessage;
                input.closest('.form-row').classList.add('is-invalid')
                count++
            }
        }
        if (count > 0) {
            return false
        }else {
            return true
        }
    }
    checkCheckBoxes() {
        const cbRequired = document.getElementsByClassName('form-row cb-required')[0]
        if(cbRequired){
            const error = cbRequired.getElementsByClassName('invalid-text')[0]
            const form_data = new FormData(document.querySelector("form"));
            if(!form_data.has(cbRequired.querySelector("input").getAttribute("name"))){
                error.textContent = `Selecteer een ${cbRequired.querySelector("input").getAttribute("name")}`;
                cbRequired.classList.add('is-invalid')
                return false;
            }
            else{
                cbRequired.classList.remove('is-invalid')
                error.textContent = "";
                return true;
            }
        }

    }

    removeDuplicates(arr) {
        var unique = [];
        arr.forEach(element => {
            if (!unique.includes(element)) {
                unique.push(element);
            }
        })
        return unique
    }

    toggleInputNoEmail(e) {
        const fieldEmail = document.getElementById("id_email_melder")
        const fieldPhone = document.getElementById("id_telefoon_melder")
        const labelEmail = document.querySelector("label[for='id_email_melder']");
        const labelPhone = document.querySelector("label[for='id_telefoon_melder']");
        const labelEmailTextClean = labelEmail.innerHTML.split("<small>")[0]
        const labelPhoneTextClean = labelPhone.innerHTML.split("<small>")[0]

        if(e.target.checked) {
            //no email, phone required
            fieldEmail.removeAttribute("required")
            fieldEmail.setAttribute("disabled", true)
            fieldEmail.value = ""
            fieldPhone.setAttribute("required", true)
            //show/hide helptext
            labelEmail.innerHTML = `${labelEmailTextClean} <small>(Niet verplicht)</small>`
            labelPhone.innerHTML = `${labelPhoneTextClean}`

        } else {
            //use email, phone NOT required
            fieldPhone.removeAttribute("required")
            fieldEmail.setAttribute("required", true)
            fieldEmail.removeAttribute("disabled", "disabled")
            labelEmail.innerHTML = `${labelEmailTextClean}`
            labelPhone.innerHTML = `${labelPhoneTextClean} <small>(Niet verplicht)</small>`
            //show/hide helptext
        }


    }

    checkSpecifiekGraf(){
        const specifiekGrafCategorieen = JSON.parse(this.specifiekGrafCategorieenValue)
        if(specifiek_graf === 0) {
            this.hideField("id_grafnummer")
            this.hideField("id_naam_overledene")
            this.hideField("id_rechthebbende")
        } else {
            this.showField("id_grafnummer")
            this.showField("id_naam_overledene")
            this.showField("id_rechthebbende")
        }

        let checkBoxes = document.querySelectorAll(`[name="categorie"]`)
        let catIdsToShow = specifiekGrafCategorieen[specifiek_graf]
        for (let i=0; i<checkBoxes.length; i++){
            if (catIdsToShow.includes(checkBoxes[i].value)){
                this.showCheckbox(checkBoxes[i])
            }else {
                this.hideCheckbox(checkBoxes[i])
            }
        }
    }
    onSpecifiekGrafChange(e){
        specifiek_graf = Number(e.target.value)
        this.checkSpecifiekGraf()
    }

    hideCheckbox(cbToHide){
        cbToHide.checked = false
        cbToHide.setAttribute("disabled", "disabled")
        cbToHide.closest('li').style.display="none";
    }

    showCheckbox(cbToShow){
        cbToShow.removeAttribute("disabled")
        cbToShow.closest('li').style.display="block";
    }

    hideField(fieldId) {

        const field = document.getElementById(fieldId)
        field.closest('.form-row').classList.add('hidden')
        field.value = ''
        if(field.nodeName.toLowerCase() === 'input') {
            field.removeAttribute('required')
        } else {
            //find nested inputs
            const inputList = field.getElementsByTagName('input')
            for (let i=0; i<inputList.length; i++){
                inputList[i].removeAttribute('required')
            }

        }
    }

    showField(field) {
        document.getElementById(field).closest('.form-row').classList.remove('hidden')
        document.getElementById(field).setAttribute('required', true)
    }

    onBegraafplaatsChange(e) {
        const medewerkers = JSON.parse(this.medewerkersValue)
        let options = this.aannemerFieldTarget.getElementsByTagName('option');
        const medewerkerOptions = medewerkers[e.target.value]
        this.aannemerFieldTarget.removeAttribute("disabled", "disabled")
        this.aannemerFieldTarget.setAttribute("required", "true")
        for (var i=options.length; i--;) {
            this.aannemerFieldTarget.removeChild(options[i]);
        }
        for (let i = 0; i < medewerkerOptions.length; i++){
            let option = document.createElement("OPTION")
            option.innerHTML = medewerkerOptions[i][1]
            option.setAttribute("value", medewerkerOptions[i][0])
            this.aannemerFieldTarget.appendChild(option);
        }
    }

    showFileInput() {
        const inputContainer = document.getElementById('id_fotos').parentElement;
        inputContainer.classList.remove('hidden');
        const preview = document.getElementById('imagesPreview');
    }

    removeFile (e) {
        const index = e.params.index;
        const input = document.getElementById('id_fotos')
        const fileListArr = [...input.files]
        fileListArr.splice(index, 1)
        /** Code from: https://stackoverflow.com/a/47172409/8145428 */
        const dT = new ClipboardEvent('').clipboardData || // Firefox < 62 workaround exploiting https://bugzilla.mozilla.org/show_bug.cgi?id=1422655
        new DataTransfer(); // specs compliant (as of March 2018 only Chrome)

        for (let file of fileListArr) { dT.items.add(file); }
        input.files = dT.files;
        this.updateImageDisplay();

    }

    updateImageDisplay() {
        const input = document.getElementById('id_fotos')
        const preview = document.getElementById('imagesPreview');
        const currentFiles = input.files;

        const fileTypes = [
            "image/apng",
            "image/bmp",
            "image/gif",
            "image/jpeg",
            "image/pjpeg",
            "image/png",
            "image/svg+xml",
            "image/tiff",
            "image/webp",
            "image/x-icon"
        ];

        function validFileType(file) {
            return fileTypes.includes(file.type);
        }

        function returnFileSize(number) {
            if (number < 1024) {
              return `${number} bytes`;
            } else if (number >= 1024 && number < 1048576) {
              return `${(number / 1024).toFixed(1)} KB`;
            } else if (number >= 1048576) {
              return `${(number / 1048576).toFixed(1)} MB`;
            }
        }

        while(preview.firstChild) {
            preview.removeChild(preview.firstChild);
        }

        if (currentFiles.length > 0) {

            const list = document.createElement('ul');
            list.classList.add('list-clean')
            preview.appendChild(list);

            for (const [index, file] of [...currentFiles].entries()) {
                const listItem = document.createElement('li');
                const content = document.createElement('span');
                const remove = document.createElement('button');
                remove.setAttribute('type', "button")
                remove.setAttribute('data-action', "request#removeFile")
                remove.setAttribute('data-request-index-param', index)
                remove.classList.add('btn-close')

                if (validFileType(file)) {
                    content.innerHTML = `${file.name} <small>${returnFileSize(file.size)}</small>`;
                    const image = document.createElement('img');
                    image.src = URL.createObjectURL(file);
                    image.onload = () => {
                        URL.revokeObjectURL(image.src);
                    };
                    listItem.appendChild(image);
                    listItem.appendChild(content);
                    listItem.appendChild(remove);
                } else {
                    content.textContent = `Het bestand "${file.name}" is geen geldig bestandstype. Selecteer alleen bestanden van het type "jpg, jpeg of png"`;
                    listItem.appendChild(content);
                }

                list.appendChild(listItem);
            }
        }
    }
}
