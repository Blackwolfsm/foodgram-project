class Favorites {
    constructor(config, api) {
        this.config = config;
        this.api = api;
    }

    addFavorites (target,cardId,csrftoken,callBack) {
        target.setAttribute('disabled', true)
        this.api.addFavorites(cardId,csrftoken)
            .then( e => {
                target.innerHTML = this.config.active.text;
                target.removeAttribute(this.config.attr);
                callBack&&callBack()
            })
            .finally(e => {
                target.removeAttribute('disabled');
            })
    };
    removeFavorites (target,cardId,csrftoken,callBack) {
        target.setAttribute('disabled', true)
        this.api.removeFavorites(cardId,csrftoken)
            .then( e => {
                target.innerHTML = this.config.default.text;
                target.setAttribute(this.config.attr, true);
                callBack&&callBack()
            })
            .finally(e => {
                target.removeAttribute('disabled');
            })
    };
}
