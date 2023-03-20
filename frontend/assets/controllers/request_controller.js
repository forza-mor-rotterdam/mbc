import { Controller } from '@hotwired/stimulus';

export default class extends Controller {

    static targets = ["categoryDescription"]

    connect() {
        console.log('request_controller connected')
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
        // TODO fix with turbo-frame and POST
        if(e.target.value === "categorie_andere_oorzaken"){
            this.categoryDescriptionTarget.classList.toggle('hidden')
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
