import { Controller } from '@hotwired/stimulus';

let specifiek_graf = 1
export default class extends Controller {

    static targets = ["categorieOmschrijvingField", "aannemerField", "specifiekGrafField"]
    static values = {
        medewerkers: String
    }

    connect() {
        this.aannemerFieldTarget.setAttribute("disabled", "disabled")
        this.categorieOmschrijvingFieldTarget.closest('.form-row').classList.add("hidden")
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
                this.categorieOmschrijvingFieldTarget.setAttribute('required', true)
            }else {
                fieldContainer.classList.add('hidden')
                this.categorieOmschrijvingFieldTarget.setAttribute('required', false)
            }

        }
    }

    onSpecifiekGrafChange(e){
        specifiek_graf = Number(e.target.value)
        if(specifiek_graf === 0) {
            //hide fields
            this.hideField("id_grafnummer")
            this.hideField("id_naam_overledene")
            this.hideField("id_rechthebbende")
        } else {
            this.showField("id_grafnummer")
            this.showField("id_naam_overledene")
            this.showField("id_rechthebbende")
        }
    }

    hideField(field) {
        document.getElementById(field).closest('.form-row').classList.add('hidden')
        document.getElementById(field).setAttribute('required', false)
        document.getElementById(field).value = ''

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
    onChangeSendForm(e) {
        console.log("Send form")
        // document.getElementById('requestForm').requestSubmit()
    }

    showFileInput() {
        const inputContainer = document.getElementById('id_fotos').parentElement;

        inputContainer.classList.remove('hidden');
        const preview = document.getElementById('imagesPreview');


        console.log('preview', preview)
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
