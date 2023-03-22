import { Controller } from '@hotwired/stimulus';

let specifiek_graf = 1
let form = null
let inputList = null
let checkboxList = null
let formData = null
const defaultErrorMessage = "Vul a.u.b. dit veld in."
export default class extends Controller {

    static targets = ["categorieOmschrijvingField", "aannemerField", "specifiekGrafField"]
    static values = {
        medewerkers: String
    }

    connect() {
        this.aannemerFieldTarget.setAttribute("disabled", "disabled")
        this.categorieOmschrijvingFieldTarget.closest('.form-row').classList.add("hidden")

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
        console.log('checkCheckBoxes')
        const cbRequired = document.getElementsByClassName('form-row cb-required')[0]
        if(cbRequired){
            const error = cbRequired.getElementsByClassName('invalid-text')[0]
            const form_data = new FormData(document.querySelector("form"));
            console.log(form_data)
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
    toggleInputOtherCategory(e) {
        if(e.target.value === "categorie_andere_oorzaken"){
            const fieldContainer = this.categorieOmschrijvingFieldTarget.closest('.form-row')
            if(e.target.checked) {
                fieldContainer.classList.remove('hidden')
                if(fieldContainer.getElementsByTagName('small').length > 0){
                    fieldContainer.getElementsByTagName('small')[0].remove()
                }
                this.showField("id_omschrijving_andere_oorzaken")
            }else {
                this.hideField("id_omschrijving_andere_oorzaken")
            }
        }
    }

    checkSpecifiekGraf(){
        if(specifiek_graf === 0) {
            //hide fields
            this.hideField("id_grafnummer")
            this.hideField("id_naam_overledene")
            this.hideField("id_rechthebbende")
            this.hideCheckbox("categorie_verzakking_eigen_graf")
            this.hideCheckbox("categorie_zerk_reinigen")
            this.showCheckbox("categorie_verzakking_algemeen")
        } else {
            this.showField("id_grafnummer")
            this.showField("id_naam_overledene")
            this.showField("id_rechthebbende")
            this.showCheckbox("categorie_verzakking_eigen_graf")
            this.showCheckbox("categorie_zerk_reinigen")
            this.hideCheckbox("categorie_verzakking_algemeen")
        }
    }

    onSpecifiekGrafChange(e){
        specifiek_graf = Number(e.target.value)
        this.checkSpecifiekGraf()
    }

    hideCheckbox(cbValue){
        const cbToHide = document.querySelector(`[value=${cbValue}]`);
        cbToHide.checked = false
        cbToHide.setAttribute("disabled", "disabled")
        cbToHide.closest('li').style.display="none";
    }

    showCheckbox(cbValue){
        const cbToShow = document.querySelector(`[value=${cbValue}]`);
        cbToShow.removeAttribute("disabled")
        cbToShow.closest('li').style.display="block";
    }

    hideField(fieldId) {

        const field = document.getElementById(fieldId)
        field.closest('.form-row').classList.add('hidden')
        field.value = ''
        console.log('field.nodeName', field.nodeName)
        if(field.nodeName.toLowerCase() === 'input') {
            field.removeAttribute('required')
        } else {
            //find nested inputs
            const inputList = field.getElementsByTagName('input')
            for (let i=0; i<inputList.length; i++){
                inputList[i].removeAttribute('required')
            }

        }
        console.log('hideField', field)
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
