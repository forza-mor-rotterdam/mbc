import { Controller } from '@hotwired/stimulus';

export default class extends Controller {

    static targets = ["categoryDescription"]

    connect() {
        console.log('request_controller connected')
    }

    toggleInputOtherCategory(e) {
        // TODO fix with turbo-frame and POST
        if(e.target.value === "categorie_andere_oorzaken"){
            this.categoryDescriptionTarget.classList.toggle('hidden')
        }
    }

    showFileInput() {
        const inputContainer = document.getElementById('bestanden').parentElement;

        inputContainer.classList.remove('hidden');
        const preview = document.getElementById('imagesPreview');


        console.log('preview', preview)
    }

    updateImageDisplay() {
        const input = document.getElementById('bestanden')
        const preview = document.getElementById('imagesPreview');
        const currentFiles = input.files;


        input.addEventListener('change', removeFile)

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

        const removeFile = () => {
            console.log(fileListArr)

            const fileListArr = [...input.files]
            fileListArr.splice(1, 1)
        }

        while(preview.firstChild) {
            preview.removeChild(preview.firstChild);
        }

        if (currentFiles.length > 0) {

            const list = document.createElement('ul');
            list.classList.add('list-clean')
            preview.appendChild(list);

            for (const file of currentFiles) {
              const listItem = document.createElement('li');
              const content = document.createElement('span');
              const remove = document.createElement('button');
              remove.setAttribute('type', "button")
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
