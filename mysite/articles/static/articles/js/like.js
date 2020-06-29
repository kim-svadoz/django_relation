const likeButton = document.querySelectorAll('.like-button')
likeButton.forEach(button =>{
    button.addEventListener('click', function(event){
        const articleId = event.target.dataset.id
        const likeCount = document.querySelector(`.like-count-${articleId}`)

        $httpProvider.defaults.xsrfCookieName = 'csrftoken';
        $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken'

        axios.post(`/articles/${articleId}/like/`)
        .then(response => {
            likeCount.innerText = response.data.count
            if(response.data.liked){
                event.target.className = 'fas fa-thumbs-up like-button'
                event.target.style.color = 'crimson'
            } else{
                event.target.className = 'fas fa-thumbs-down like-button'
                event.target.style.color = 'black'
            }
        })
    })
})