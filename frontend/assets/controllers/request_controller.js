import { Controller } from '@hotwired/stimulus';

export default class extends Controller {

    static targets = ["categoryDescription"]

    connect() {
        console.log('request_controller connected')
    }

    toggleInputOtherCategory(e) {
        // TODO fix with turbo-frame and POST
        if(e.target.value === "categorie_overig"){
            this.categoryDescriptionTarget.classList.toggle('hidden')
        }
    }
}
