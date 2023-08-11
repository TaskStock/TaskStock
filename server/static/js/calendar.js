let nav = 0;
let clicked = null;
let dayString = '';
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

  dayString = `${month + 1}/${day}/${year}`;

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
  const displayMonth = String(month + 1);
  const ddisplayMonth = displayMonth.padStart(2, '0');
  document.querySelector('.monthDisplay--month').innerText = `${ddisplayMonth}`;
//   document.querySelector('.monthDisplay--year').innerText = `${year}`;

  calendar.innerHTML = '';

  for(let i = 1; i <= paddingDays + daysInMonth; i++) {
    const daySquare = document.createElement('div');
    daySquare.classList.add('day');

    
    if (i > paddingDays) {
        daySquare.innerText = i - paddingDays;
        daySquare.addEventListener('click', async() => {
            // 각 day 클릭할 때 발생한는 함수 
            dayString = `${month+1}/${i-paddingDays}/${year}`; // '8/10/2023'
            
            // ajax로 dayString 보내기 
            const formData = new FormData();
            formData.append('str', dayString);

            formData.append("username", global_chart_target_username);

            const url = `/main/click_date/`;
            const res = await fetch(url, {
                method: 'POST', 
                headers: {},
                body: formData,
            })
            const {todos: todos} = await res.json();
            handleDateResponse(todos);

        
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

function handleDateResponse(todos){
    const currentInput = document.querySelector('#todo-paint');
    currentInput.innerHTML = "";
    
    if(todos.length > 0){
        for (const todo of todos){
            let paintedLevel = '';
            let emptyLevel = '';
            todo.level = Number(todo.level);
            if (todo.goal_check == true){
                todo.goal_check = 'True';
            }else{
                todo.goal_check = 'False';
            }
            for(p = 1; p < todo.level + 1; p++){
                paintedLevel += `<div level="${p}" class="active"></div>`;
            }
            for(e = todo.level + 1; e < 6; e++){
                emptyLevel += `<div level="${e}"></div>`;
            }
            // document.querySelector('.todo-add--date').innerHTML = `
            //     ${todo.month}월 ${todo.date}일
            // `;
            currentInput.innerHTML += `
            <div class="todo-item todo-item-${todo.id} ">
                        
                <div class="todo-checkbox todo-checkbox-${todo.id} ${todo.goal_check}" onclick="check_todo(${todo.id})"></div>
                
                <input type="text" class="todo-contents" onclick="edit_todo(${todo.id})" value="${todo.content}" readonly>
                <div class="todo-level todo-level-${todo.id}">
                    ${paintedLevel}
                    ${emptyLevel}
                </div>
                <!-- edit page -->
                <div class="todo-item--edit todo-item--edit-${todo.id}">
                    <div class="todo-item--date">${todo.month}월 ${todo.date}일</div>
                    <div class="todo-item--input">
                        <span>할 일을 수정하세요</span>
                        <input type="text" placeholder="${todo.content}" value="${todo.content}">
                    </div>
                    <div class="todo-item--level">
                        <span>난이도를 수정하세요</span>
                        <div class="edit-todo-level" curr-level="${todo.level}">
                            <div level="1"></div>
                            <div level="2"></div>
                            <div level="3"></div>
                            <div level="4"></div>
                            <div level="5"></div>
                        </div>
                    </div>
                    <div class="edit-btn--container">
                        <div class="todo-edit--delete-btn" onclick="delete_todo(${todo.id})">삭제</div>
                        <div class="todo-edit--submit-btn" onclick="update_todo(${todo.id})">완료</div>
                    </div>
                </div>
            </div>`;


        }
    }

}


function clickedDayString(dayString){
    return dayString;
}

function initButtons() {
  document.getElementById('nextButton').addEventListener('click', () => {
    nav++;
    load();
    blackBorder();
  });

  document.getElementById('backButton').addEventListener('click', () => {
    nav--;
    load();
    blackBorder();
  });
}

function blackBorder(){
    document.querySelectorAll('.cal--calendar .day').forEach(day => {
        day.addEventListener('click', () => {
            paintDate();
            const clicked_day = document.querySelectorAll('.clickedDay');
          
            if(clicked_day.length !== 0){
                clicked_day.forEach(c => {
                    c.classList.remove('clickedDay');
                })
                
            }
            day.classList.add('clickedDay');
        })
    })
}
function paintDate(){
    let clicked_month = dayString.split('/')[0];
    let clicked_date = dayString.split('/')[1];
    
    document.querySelector('.todo-add--date').innerHTML = `
        ${clicked_month}월 ${clicked_date}일
    `;
    const items = document.querySelectorAll('.todo-item--date');
    console.log(items.length);
    if (items.length !== 0){
        items.forEach(i => {
            i.innerHTML = `
            ${clicked_month}월 ${clicked_date}일
        `;
        })
    }
   
    
    
}
initButtons();
load();
blackBorder();
paintDate();



