// rotating the hamburger btn when clicked
const hamburgerBtn = document.querySelector(".navbar-toggler")
hamburgerBtn.addEventListener('click', function(){
    hamburgerBtn.classList.toggle("rotate")
})

// updating the date in the footer
const date = document.getElementById("date")
date.innerHTML = new Date().getFullYear()