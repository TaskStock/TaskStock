const hamburger = document.querySelector('.hamburger');
const contents = document.querySelector('.hamburger-contents');

hamburger.addEventListener('click', () => {
    hamburger.classList.toggle('active');
})