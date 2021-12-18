
// rotating the hamburger btn when clicked
const hamburgerBtn = document.querySelector(".navbar-toggler")
hamburgerBtn.addEventListener('click', function(){
    if (hamburgerBtn.classList.contains('rotate')) {
        hamburgerBtn.classList.remove('rotate')
        hamburgerBtn.classList.add("rotate-reverse")
    } else {
        hamburgerBtn.classList.remove("rotate-reverse")
        hamburgerBtn.classList.add('rotate')
    }
})

// updating the date in the footer
const date = document.getElementById("date")
date.innerHTML = new Date().getFullYear()
