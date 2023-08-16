const hamburger = document.querySelector('.hamburger');
const contents = document.querySelector('.hamburger-contents');

hamburger.addEventListener('click', () => {
    hamburger.classList.toggle('active');
})

// 문서 전체에 클릭 이벤트 리스너 추가
document.addEventListener('click', (event) => {
    // 클릭된 요소가 hamburger contents 내부에 속하는지 확인
    let clickedInsideEditContainer = false;
    
    if (contents.contains(event.target) || event.target.parentNode.classList.contains('hamburger') || event.target.classList.contains('hamburger')) {
        clickedInsideEditContainer = true;
    }

    // 클릭된 요소가 editContainer 내부에 속하지 않는 경우 모든 editContainer의 'active' 클래스 제거
    if (!clickedInsideEditContainer) {
        hamburger.classList.remove('active');
    }
});

//  mobile hamburger
const left_section = document.querySelector('section');
const tb_section = document.querySelector('#tb-section');

document.querySelector('#hamburger-tb').addEventListener('click', () => {
    left_section.style.left = '-350px';
    
})
document.querySelector('#tb-hamburger').addEventListener('click', () => {
    left_section.style.left = '0';    
    tb_section.style.left = '-70px';
})

// dark mode toggle
const bodyEl = document.querySelector('body');
const darkBtn = document.querySelector('.menu-right__darkmode');
const activeTheme = localStorage.getItem('theme');

if(activeTheme){
    bodyEl.classList.add('dark');
    darkBtn.querySelector('i').classList.remove('gg-moon');
    darkBtn.querySelector('i').classList.add('gg-sun');
    darkBtn.querySelector('span').innerHTML = 'Light Mode';
}

darkBtn.addEventListener('click', () => {
    bodyEl.classList.toggle('dark');
   
    if(bodyEl.classList.contains('dark')){
        localStorage.setItem('theme', 'dark');
        darkBtn.querySelector('i').classList.remove('gg-moon');
        darkBtn.querySelector('i').classList.add('gg-sun');
        darkBtn.querySelector('span').innerHTML = 'Light Mode';
    }else{
        localStorage.removeItem('theme');
        darkBtn.querySelector('i').classList.remove('gg-sun');
        darkBtn.querySelector('i').classList.add('gg-moon');
        darkBtn.querySelector('span').innerHTML = 'Dark Mode';
    }
})


// mobile에서 chart, calendar 탭
// const mb_chartBtn = document.querySelector('#mb-nav--chart + label');
// const mb_chartBtn_input = document.querySelector('#mb-nav--chart');
// const mb_calBtn = document.querySelector('#mb-nav--calendar + label');
// const mb_calBtn_input = document.querySelector('#mb-nav--calendar');

// document.querySelector('#mb-main--nav').addEventListener('click', () => {
//     mb_tab();
// })
// function mb_tab(){
//     if (window.matchMedia("(max-width: 600px)").matches) {
//         if(mb_chartBtn_input.checked == true){
//             document.querySelector('.main-right').style.display = 'none';
//             document.querySelector('.main-left').style.display = 'flex';
//         }
//         else if(mb_chartBtn_input.checked == false){
//             document.querySelector('.main-left').style.display = 'none';
//             document.querySelector('.main-right').style.display = 'block';
//         }
//     }
// }
// mb_tab();

if (window.matchMedia("(max-width: 600px)").matches) {
    const mb_ccBtn = document.querySelector('#mb-main--nav');
    mb_ccBtn.addEventListener('click', () => {
        mb_tab();
    })
    mb_tab();
}
function mb_tab(){
    if (window.matchMedia("(max-width: 600px)").matches) {
        const mb_ccBtn = document.querySelector('#mb-main--nav');
        mb_ccBtn.classList.toggle('cal');
        if(mb_ccBtn.classList.contains('cal')){
            mb_ccBtn.innerHTML = '<i class="fa-regular fa-calendar-check"></i>';
            document.querySelector('.main-right').style.display = 'none';
            document.querySelector('.main-left').style.display = 'flex';
        }else{
            mb_ccBtn.innerHTML = '<i class="fa-solid fa-chart-line"></i>';
            document.querySelector('.main-left').style.display = 'none';
            document.querySelector('.main-right').style.display = 'block';
        }
    }
}

