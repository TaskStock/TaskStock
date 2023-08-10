let nav = 0;
let clicked = null;

const calendar = document.querySelector('.cal--calendar');
const weekdays = ['일요일', '월요일', '화요일', '수요일', '목요일', '금요일', '토요일'];

function load() {
  const dt = new Date();

  if (nav !== 0) {
    dt.setMonth(new Date().getMonth() + nav);
  }

  const day = dt.getDate();
  const month = dt.getMonth();
  const year = dt.getFullYear();

  // first day
  const firstDayOfMonth = new Date(year, month, 1);
  // last day 
  const daysInMonth = new Date(year, month + 1, 0).getDate(); 
  
  const dateString = firstDayOfMonth.toLocaleDateString('ko-kr', {
    weekday: 'long',
    year: 'numeric',
    month: 'numeric',
    day: 'numeric',
  }); // 2023. 8. 1. 화요일
  
  const paddingDays = weekdays.indexOf(dateString.split('. ')[3]); // 2
  
  document.getElementById('monthDisplay').innerText = `${year}년 ${month + 1}월`;

  calendar.innerHTML = '';

  for(let i = 1; i <= paddingDays + daysInMonth; i++) {
    const daySquare = document.createElement('div');
    daySquare.classList.add('day');

    if (i > paddingDays) {
        daySquare.innerText = i - paddingDays;
        daySquare.addEventListener('click', () => {
            // 각 day 클릭할 때 발생한는 함수 
            console.log('click');
        })
        if (i - paddingDays === day && nav === 0) {
            daySquare.id = 'currentDay';
        }

    } else {
      daySquare.classList.add('padding');
    }

    calendar.appendChild(daySquare);    
  }
}


function initButtons() {
  document.getElementById('nextButton').addEventListener('click', () => {
    nav++;
    load();
  });

  document.getElementById('backButton').addEventListener('click', () => {
    nav--;
    load();
  });
}

initButtons();
load();