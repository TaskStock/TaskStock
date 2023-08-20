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
  document.querySelector('.monthDisplay--year').innerText = `${year}`;

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
            const {todos: todos, category_datas: category_datas} = await res.json();
            handleDateResponse(todos, category_datas);
            has_unchecked_todos();
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

function delayTodoButton(){
    // 연속으로 클릭하지 못하도록 설정
    const checkBoxes = document.querySelectorAll(`.todo-checkbox`);
    checkBoxes.forEach(checkBox => {
        checkBox.addEventListener('click', () => {
            if (!checkBox.classList.contains('disabled')) {
                checkBox.classList.add('disabled'); // 클릭된 요소를 비활성화 스타일로 변경
    
                // 1초(1000 밀리초) 후에 요소 다시 활성화 스타일로 변경
                setTimeout(() => {
                    checkBox.classList.remove('disabled');
                }, 1500);
            }
        });
    });
}

function handleDateResponse(todos, category_datas){
    const currentInput = document.querySelector('#todo-paint');
    currentInput.innerHTML = "";
    
    if(todos.length > 0){        
        for (const todo of todos){
            let category_html="";
            for (const c_name of category_datas) {
                if(todo.category==c_name)
                    category_html+=`<option value='${c_name}' selected>${c_name}</option>`;
                else
                    category_html+=`<option value='${c_name}'>${c_name}</option>`;
            }
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

            if(global_chart_target_username != global_current_username){
                currentInput.innerHTML += `
                <div class="todo-item todo-item-${todo.id}">
                    <div class="todo-checkbox todo-checkbox-${todo.id} ${todo.goal_check}"></div>
                    
                    <input type="text" 
                        class="todo-contents" 
                        onclick="edit_todo(${todo.id})"
                        value="${todo.content}"
                        readonly>
                    <div class="todo-level todo-level-${todo.id}">
                        ${paintedLevel}
                        ${emptyLevel}
                    </div>
                    
                </div>
                `;
            }else{
                currentInput.innerHTML += `
                <div class="todo-item todo-item-${todo.id}">
                    <div class="todo-checkbox todo-checkbox-${todo.id} ${todo.goal_check}" onclick="check_todo(${todo.id})"></div>
                    
                    <input type="text" 
                        class="todo-contents" 
                        onclick="edit_todo(${todo.id})"
                        value="${todo.content}"
                        readonly>
                    <div class="todo-level todo-level-${todo.id}">
                        ${paintedLevel}
                        ${emptyLevel}
                    </div>
                    
                    <div class="todo-item--edit todo-item--edit-${todo.id}">
                        <div class="todo-item--date"></div>
                        <div class="todo-item--input">
                            <span>할 일을 수정하세요</span>
                            <input type="text"
                            placeholder="${todo.content}"
                            value="${todo.content}"
                            >
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
                        <div class="todo-edit--category">
                            <span>카테고리를 수정하세요</span>
                            <select class="todo-edit--select">
                                <option value="">None</option>
                                ${category_html}
                            </select>
                        </div>
                        <div class="edit-btn--container">
                            <div class="todo-edit--delete-btn" onclick="delete_todo(${todo.id})">삭제</div>
                            <div class="todo-edit--submit-btn" onclick="update_todo(${todo.id})">완료</div>
                        </div>
                    </div>
                </div>
                `;
            }

        }
        delayTodoButton();
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
    
    add_date=document.querySelector('.todo-add--date')
    if(add_date != null){
        add_date.innerHTML = `
            ${clicked_month}월 ${clicked_date}일
        `;
    }
    const items = document.querySelectorAll('.todo-item--date');

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

