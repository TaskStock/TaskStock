
// 문서 전체에 클릭 이벤트 리스너 추가
if (window.matchMedia("(min-width: 1081px)").matches){
    const hamburger = document.querySelector('.hamburger');
    const contents = document.querySelector('.hamburger-contents');
    
    hamburger.addEventListener('click', () => {
        hamburger.classList.toggle('active');
    })
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
}

//  tablet hamburger
const left_section = document.querySelector('section');
const tb_section = document.querySelector('#tb-section');

document.querySelector('#hamburger-tb').addEventListener('click', () => {
    left_section.style.left = '-350px';
    
})
document.querySelector('#tb-hamburger').addEventListener('click', () => {
    left_section.style.left = '0';    
    tb_section.style.left = '-70px';
})
if (window.matchMedia("(min-width: 900px) and (max-width: 1080px)").matches){
    const tb_section = document.querySelector('section');
    const tb_small_section = document.querySelector('#tb-section');
    document.addEventListener('click', (event) => {
        // 클릭된 요소가 tb_hamburger contents 내부에 속하는지 확인
        let clickedInsideEditContainer = false;
        // console.log(event.target);
        if (tb_section.contains(event.target) || tb_small_section.contains(event.target)) {
            clickedInsideEditContainer = true;
        }

        // 클릭된 요소가 editContainer 내부에 속하지 않는 경우 section 넣기
        if (!clickedInsideEditContainer) {
            left_section.style.left = '-350px';
        }
    });
}




// dark mode toggle
const bodyEl = document.querySelector('body');
const darkBtn = document.querySelectorAll('.menu-right__darkmode');
const activeTheme = localStorage.getItem('theme');

if(activeTheme){
    bodyEl.classList.add('dark');
    darkBtn.forEach(btn => {
        btn.querySelector('i').classList.remove('gg-moon');
        btn.querySelector('i').classList.add('gg-sun');
        btn.querySelector('span').innerHTML = 'Light Mode';
    })
}

darkBtn.forEach(btn => {
    btn.addEventListener('click', () => {
        bodyEl.classList.toggle('dark');
        // console.log('clicked');
    
        if(bodyEl.classList.contains('dark')){
            localStorage.setItem('theme', 'dark');
            btn.querySelector('i').classList.remove('gg-moon');
            btn.querySelector('i').classList.add('gg-sun');
            btn.querySelector('span').innerHTML = 'Light Mode';
        }else{
            localStorage.removeItem('theme');
            btn.querySelector('i').classList.remove('gg-sun');
            btn.querySelector('i').classList.add('gg-moon');
            btn.querySelector('span').innerHTML = 'Dark Mode';
        }
        if (window.matchMedia("(max-width: 600px)").matches){
            document.querySelector('#mb--header .gg-menu-right-alt').classList.toggle('active');
            document.querySelector('#tb-section').style.right = '-100%';
        }        
})})

if (window.matchMedia("(max-width: 600px)").matches){
    // 모바일 햄버거 왼쪽
    const mb_hbg_left = document.querySelector('#mb--header .gg-menu-left-alt');
    const mb_hbg_right = document.querySelector('#mb--header .gg-menu-right-alt');
    const right_section = document.querySelector('#tb-section');
    mb_hbg_left.addEventListener('click', () => {
        mb_hbg_left.classList.toggle('active');
        if(mb_hbg_left.classList.contains('active')){
            left_section.style.left = '0';    
            right_section.style.right = '-100%';
        }else{
            left_section.style.left = '-90%';   
        } 
    })
    mb_hbg_right.addEventListener('click', () => {
        mb_hbg_right.classList.toggle('active');
        if(mb_hbg_right.classList.contains('active')){
            right_section.style.right = '-10%';
            left_section.style.left = '-90%'; 
        }else{
            right_section.style.right = '-100%';
        }
    })

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

