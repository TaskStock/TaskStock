// set todo-add--container width 
const plus = document.querySelector('.todo-plus--btn');
const container = document.querySelector('.main-right--container');
const add_container = document.querySelector('.todo-add--container');
const edit_containers = document.querySelectorAll('.todo-item--edit');
let Add_width = container.clientWidth * 0.8; 
let Edit_width = container.clientWidth * 0.9; 
let Add_right = Add_width + 30;
if(add_container != null){
    add_container.style.width = `${Add_width}px`;
    add_container.style.left = `80px`;
}
edit_containers.forEach(box => {
    box.style.width = `${Edit_width}px`;
})

// add todo 
let level = '0';
const level_stars = document.querySelectorAll('.sel-todo-level div');
level_stars.forEach(star => {
    star.addEventListener('click', () => {
        level = star.getAttribute('level');
        paintStar(level);
    }
)})

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


function paintStar(level){
    document.querySelectorAll('.sel-todo-level div').forEach(star => {
        if (star.getAttribute('level') <= level){
            star.classList.add('active');
        } else{
            star.classList.remove('active');
        }
    })
}

if(plus != null){
    plus.addEventListener('click', () => {
        document.querySelector('.todo-plus').classList.toggle('active');
        setTimeout(() => {
            document.querySelector('.todo-add--input input').focus();
        }, 500);

        // // 오류메세지 초기화
        document.querySelector(`.todo-add--container .todo-add--input span`).style.color = '#fff';
        document.querySelector(`.todo-add--container .todo-add--level span`).style.color = '#fff';

    });
}


const add_todo = async(date_id) => {
    const url = '/main/add_todo/';
    let inputTag = document.querySelector('.todo-add--input input');
    let inputVal = inputTag.value;

    // 달력에서 클릭한 날짜. 클릭 안했으면 오늘날짜 
    let click_date = clickedDayString(dayString);
    // console.log(click_date);

    const selectElement = document.querySelector('#todo-add--select');
    category_name=selectElement.value;
    selectElement.value="";
    
    const data = { 
        content: inputVal, 
        level: parseInt(level), 
        date_id: click_date,
        category: category_name,
        };
    if (inputVal !== '' && level !== '0'){
        const res = await fetch(url, {
            method: 'POST', 
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(data),
        })
        const {
            todo_id: todo_id,
            my_level: my_level,
            content: content, 
            category_datas: category_datas,
            value_start: valueStart,
            value_end: valueEnd,
            value_high: valueHigh,
            value_low: valueLow,
            percentage: percentage,
        } = await res.json();
        document.querySelector(`.day${date_id}--todo input`).value = '';
        level = '0';
        paintStar('0');
        document.querySelector('.todo-plus').classList.remove('active');
        handleTodoResponse(todo_id, my_level, content, category_datas, category_name, valueStart, valueEnd, valueHigh, valueLow, percentage);

    }else if (inputVal === ''){
        document.querySelector(`.day${date_id}--todo .todo-add--input span`).style.color = '#ff0033';
    }else if (level == '0'){
        document.querySelector(`.day${date_id}--todo .todo-add--level span`).style.color = '#ff0033';
    } 
}

const handleTodoResponse = async(todo_id, level, content, category_datas, category_name, valueStart, valueEnd, valueHigh, valueLow, percentage) => {
    let paintedLevel = '';
    let emptyLevel = '';
    level = Number(level);
    for(p = 1; p < level + 1; p++){
        paintedLevel += `<div level="${p}" class="active"></div>`;
    }
    for(e = level + 1; e < 6; e++){
        emptyLevel += `<div level="${e}"></div>`;
    }

    let category_html="";
    for (const c_name of category_datas) {
        if(category_name==c_name)
            category_html+=`<option value='${c_name}' selected>${c_name}</option>`;
        else
            category_html+=`<option value='${c_name}'>${c_name}</option>`;
    }

    if(global_chart_target_username != global_current_username){
        document.querySelector('.todo-paint').innerHTML += `
        <div class="todo-item todo-item-${todo_id}">
            <div class="todo-checkbox todo-checkbox-${todo_id}" onclick="check_todo(${todo_id})"></div>
            
            <div class="todo-contents" onclick="edit_todo(${todo_id})">${content}</div>
            <div class="todo-level todo-level-${todo_id}">
                ${paintedLevel}
                ${emptyLevel}
            </div>
            
        </div>
        `;
    }else{
        document.querySelector('.todo-paint').innerHTML += `
        <div class="todo-item todo-item-${todo_id}">
            <div class="todo-checkbox todo-checkbox-${todo_id}" onclick="check_todo(${todo_id})"></div>
            
            <div class="todo-contents" onclick="edit_todo(${todo_id})">${content}</div>
            <div class="todo-level todo-level-${todo_id}">
                ${paintedLevel}
                ${emptyLevel}
            </div>
            
            <div class="todo-item--edit todo-item--edit-${todo_id}">
                <div class="todo-item--date"></div>
                <div class="todo-item--input">
                    <span>할 일을 수정하세요</span>
                    <input type="text"
                    placeholder="${content}"
                    value="${content}"
                    >
                </div>
                <div class="todo-item--level">
                    <span>난이도를 수정하세요</span>
                    <div class="edit-todo-level" curr-level="${level}">
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
                        <option value="">카테고리 없음</option>
                        ${category_html}
                    </select>
                </div>
                <div class="edit-btn--container">
                    <div class="todo-edit--delete-btn" onclick="delete_todo(${todo_id})">삭제</div>
                    <div class="todo-edit--submit-btn" onclick="update_todo(${todo_id})">완료</div>
                </div>
            </div>
        </div>
        `;
    }
    
    delayTodoButton();
    update_chart();
    has_unchecked_todos();
    updateValueElements(valueStart, valueEnd, valueHigh, valueLow, percentage)
}


// edit todo
let updated_level = 0;
let edited_star = false;

const edit_todo = (todo_id) => {
    // 현재 edit container가 열린 상태에서 다른 input을 클릭하면 현재 container 없어져야 하니 
    // 모두 닫고 시작하자 
    document.querySelectorAll('.todo-item--edit').forEach(c => {
        c.classList.remove('active');
    })

    // 열고 닫기
    const edit_container = document.querySelector(`.todo-item--edit-${todo_id}`);

    if(edit_container!=null){
        edit_container.classList.toggle('active');
        edit_container.style.width = `${Edit_width}px`;

        let curr_level = edit_container.querySelector(`.edit-todo-level`).getAttribute('curr-level');
        epaintStar(todo_id, curr_level);

        if(edit_container.classList.contains('active')){
            const content = edit_container.querySelector('input');
            setTimeout(() => {
                // 커서 끝으로 
                const editContent = content.value;
                content.focus();
                content.value = '';
                content.value = editContent;
            }, 500);
         
            edit_container.querySelectorAll(`.edit-todo-level > div`).forEach(star => {
                star.addEventListener('click', () => {
                    
                    updated_level = star.getAttribute('level');
                    epaintStar(todo_id, updated_level);
                    edited_star = true;
                    
                }
            )})
        }
        paintDate();
    }
}

// 문서 전체에 클릭 이벤트 리스너 추가
document.addEventListener('click', (event) => {
    // 클릭된 요소가 editContainer 내부에 속하는지 확인
    const containers = document.querySelectorAll('.todo-item');
    const editContainers = container.querySelectorAll(`.todo-item--edit`);
    
    let clickedInsideEditContainer = false;
    
    containers.forEach((container) => {
        const editContainer = container.querySelector(`.todo-item--edit`);
        
        if(editContainer!=null){
            if (editContainer.contains(event.target) || event.target.classList.contains('todo-contents')) {
                clickedInsideEditContainer = true;
            }
        }
        
    });

    // 클릭된 요소가 editContainer 내부에 속하지 않는 경우 모든 editContainer의 'active' 클래스 제거
    if (!clickedInsideEditContainer) {
        editContainers.forEach((editContainer) => {
            editContainer.classList.remove('active');
        });
        
    }
});


const update_todo = async(todo_id) => {
    const edit_container = document.querySelector(`.todo-item--edit-${todo_id}`);
    let curr_level = edit_container.querySelector(`.edit-todo-level`).getAttribute('curr-level');
    const content = edit_container.querySelector('input');
    if (edited_star === true){
        curr_level = updated_level;
        // 초기화 
        updated_level = 0;
        edited_star = false;
    }
    const curr_content = content.value;

    const category = edit_container.querySelector('.todo-edit--select');
    c_value=category.value;
    if(c_value==null)
        c_value="";

    // ajax
    const url = `/main/update_todo/${todo_id}/`;
    const res = await fetch(url, {
        method: 'POST', 
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({todo_id, curr_level, curr_content, c_value}),
    })
    
    const {
        t_id: t_id,
        c_level: c_level,
        c_content: c_content,
        value_start: valueStart,
        value_end: valueEnd,
        value_high: valueHigh,
        value_low: valueLow,
        percentage: percentage,
    } = await res.json();
    handleUpdateTodoRes(t_id, c_level, c_content, valueStart, valueEnd, valueHigh, valueLow, percentage);
    edit_container.classList.remove('active');

}

const handleUpdateTodoRes = async(todo_id, level, content, valueStart, valueEnd, valueHigh, valueLow, percentage) => {
    document.querySelector(`.todo-item-${todo_id} .todo-contents`).innerText = content;
    let paintedLevel = '';
    let emptyLevel = '';
    level = Number(level);
    for(p = 1; p < level + 1; p++){
        paintedLevel += `<div level="${p}" class="active"></div>`;
    }
    for(e = level + 1; e < 6; e++){
        emptyLevel += `<div level="${e}"></div>`;
    }
    
    const container = document.querySelector(`.todo-level-${todo_id}`);
    const edit_container = document.querySelector(`.todo-item--edit-${todo_id} .edit-todo-level`);
    edit_container.setAttribute('curr-level', level);
    
    container.innerHTML = `
            ${paintedLevel}
            ${emptyLevel}
    `;
    edit_container.innerHTML = `
            ${paintedLevel}
            ${emptyLevel}
    `;
    update_chart();
    paintDate();
    updateValueElements(valueStart, valueEnd, valueHigh, valueLow, percentage)
}

function epaintStar(todo_id, level){
    const edit_stars = document.querySelectorAll(`.todo-item--edit-${todo_id} .edit-todo-level div`);
    edit_stars.forEach(star => {
        if (star.getAttribute('level') <= level){
            star.classList.add('active');
        } else{
            star.classList.remove('active');
        }
    })
}

// delete todo

const delete_todo = async(todo_id) => {
    const url = `/main/delete_todo/${todo_id}/`;
    const res = await fetch(url, {
        method: 'POST', 
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({todo_id}),
    })
    const {
        my_combo: my_combo,
        id: id, 
        d_id: d_id, 
        todo_cnt:todo_cnt,
        value_start: valueStart,
        value_end: valueEnd,
        value_high: valueHigh,
        value_low: valueLow,
        percnet:percentage,
    } = await res.json();
    handleDelTodoRes(my_combo, id, d_id, todo_cnt, valueStart, valueEnd, valueHigh, valueLow, percentage);
}
const handleDelTodoRes = async(my_combo, todo_id, date_id, todo_cnt, valueStart, valueEnd, valueHigh, valueLow, percentage) => {
    // delete container
    const container = document.querySelector(`.todo-item-${todo_id}`);
    container.remove();
    update_chart();
    has_unchecked_todos();
    handleCombo(my_combo);
    handleCompletedTodos(todo_cnt)
    updateValueElements(valueStart, valueEnd, valueHigh, valueLow, percentage)
}



// check todo
const check_todo = async(todo_id) => {
    const checkBox = document.querySelector(`.todo-checkbox-${todo_id}`);
    if(checkBox.classList.contains('disabled')){
        return;
    }

    checkBox.classList.toggle('True');
    let status = '';
    // True || False
    if(checkBox.classList.contains('True')){
        status = 'True';
        
    }else{
        status = 'False';
    }
    
    const url = `/main/check_todo/${todo_id}/`;
    const res = await fetch(url, {
        method: 'POST', 
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({todo_id, status}),
    })
    const {
        'my_combo': my_combo,
        'color': color, 
        'todo_status': todo_status, 
        't_id': t_id, 
        'todo_cnt':todo_cnt,
        'value_start': valueStart,
        'value_end': valueEnd,
        'value_high': valueHigh,
        'value_low': valueLow,
        'user_percentage':percent
    } = await res.json();
    
    handleCheckTodoRes(my_combo, color, todo_status, t_id, todo_cnt, valueStart, valueEnd, valueHigh, valueLow, percent);
}

function handleCheckTodoRes(my_combo, color, status, todo_id, todo_cnt, valueStart, valueEnd, valueHigh, valueLow, percent){
    const checkBox = document.querySelector(`.todo-checkbox-${todo_id}`);
    if (status == 'True'){
        checkBox.classList.add('True');
    } else{
        checkBox.classList.remove('True');
    }
    // console.log("Percentage from server:", percent);
    
    handleCombo(my_combo);
    update_chart();
    has_unchecked_todos();
    handleCompletedTodos(todo_cnt);
    updateValueElements(valueStart, valueEnd, valueHigh, valueLow, percent);

}

function has_unchecked_todos(){
    // 완료하지 않은 투두가 있는 날 색칠 opacity: 0.2
    const month = document.querySelector('.monthDisplay--month').innerText;
    const year = document.querySelector('.monthDisplay--year').innerText;
    const days = document.querySelectorAll('.cal--calendar .day');

    days.forEach(d => {
        if(!d.classList.contains('padding')){
            // 8/11/2023
            let checkDayString = `${parseInt(month)}/${parseInt(d.innerText)}/${parseInt(year)}`;
            // console.log(checkDayString);
            // 해당 날짜의 todos
            const formData = new FormData();
            formData.append('str', checkDayString);
            formData.append("username", global_chart_target_username);

            const url = `/main/click_date/`;
            fetch(url, {
                method: 'POST', 
                headers: {},
                body: formData,
            }).then(res => res.json()).then(data => {
                const {todos: todos} = data;
                if(todos.length > 0){
                    let has_unchecked = false;
                    for(const todo of todos){
                        // uncheck가 하나라도 있으면, true로 바꾸기 
                        if(todo.goal_check == false){
                            has_unchecked = true;
                        }
                    }
                    if(has_unchecked == true){
                        d.classList.add('unchecked');
                    }else{
                        d.classList.remove('unchecked');
                    }
                } else if(todos.length == 0){
                    d.classList.remove('unchecked');
                }
            })
        }
    })
    
}
// 차트 다시 불러오기
function update_chart(){
    let chart_radio=localStorage.getItem('chart_radio');
    
    let chart_period;
    if(chart_radio=="7"){
        chart_period="#one_week";
    }else if(chart_radio=="30"){
        chart_period="#one_month";
    }else if(chart_radio=="90"){
        chart_period="#three_month";
    }else if(chart_radio=="180"){
        chart_period="#six_month";
    }else if(chart_radio=="365"){
        chart_period="#one_year";
    }
    
    let chart_update;
    if(chart_radio==null){
        chart_update = document.querySelector("#one_week");
    }else{
        chart_update = document.querySelector(chart_period);
    }
    chart_update.click();
}
// combo
function handleCombo(combo){
    const comboHTML = document.querySelector('.dashboard-top__cc span:nth-child(3)');
    comboHTML.innerHTML = `🔥 ${combo}`;
    comboHTML.style.animation = `combo 1.5s ease-in-out`;
    comboHTML.addEventListener('animationend', () => {
        comboHTML.style.animation = ''; // 애니메이션 제거
    }, { once: true });
}

// completed_todos
function handleCompletedTodos(todo_cnt){
    const completedTodosElement = document.querySelector('.dashboard-top__cc span:nth-child(4)');
    completedTodosElement.innerText = `✔︎ ${todo_cnt}`;
}

has_unchecked_todos();

// 

async function animateCounter(element, startValue, endValue, duration = 400, delay = 10) {
    const totalSteps = duration / delay;
    const stepValue = (endValue - startValue) / totalSteps;
    let currentValue = startValue;

    for (let i = 0; i <= totalSteps; i++) {
        element.textContent = Math.round(currentValue).toString();
        await new Promise(resolve => setTimeout(resolve, delay));
        currentValue += stepValue;
    }
}

async function updateValueElements(valueStart, valueEnd, valueHigh, valueLow, percentage) {
    const percentElement = document.querySelector('.percentage-value .counter');
    const startElement = document.querySelector("#ochl_open .counter");
    const endElement = document.querySelector("#ochl_close .counter");
    const highElement = document.querySelector("#ochl_high .counter");
    const lowElement = document.querySelector("#ochl_low .counter");
    
    const percentValueFromHTML = parseFloat(percentElement.textContent);
    const startValueFromHTML = parseFloat(startElement.textContent);
    const endValueFromHTML = parseFloat(endElement.textContent);
    const highValueFromHTML = parseFloat(highElement.textContent);
    const lowValueFromHTML = parseFloat(lowElement.textContent);

    // Animate the values
    await Promise.all([
        animateCounter(percentElement, percentValueFromHTML, percentage),
        animateCounter(startElement, startValueFromHTML, valueStart),
        animateCounter(endElement, endValueFromHTML, valueEnd),
        animateCounter(highElement, highValueFromHTML, valueHigh),
        animateCounter(lowElement, lowValueFromHTML, valueLow)
    ]);

    if (percentage !== null) {
        const displayElement = document.querySelector(".percentage-display");
        const valueElement = displayElement.querySelector(".percentage-value");
        const iconElement = document.getElementById("percentage-icon");
        const percentValue = parseFloat(percentage);
    
        valueElement.innerText = `${percentage} %`;

        if (iconElement) {
            iconElement.remove();
        }

        const misPercentageBox = document.querySelector("#mis-percentage");
        misPercentageBox.innerHTML=`
        <span class="percentage-value"><span class="counter">${percentValue}</span> %</span>
        `;
        
        if (percentValue > 0) {
            misPercentageBox.innerHTML+=`
            <i class="fa-solid fa-chevron-up" id="percentage-icon" style="color: red;"></i>
            `;
        } else if (percentValue < 0) {
            misPercentageBox.innerHTML+=`
            <i class="fa-solid fa-chevron-down" id="percentage-icon" style="color: blue;"></i>
            `;
        }
    }
}

// comma 찍기
const marketCap = document.querySelector('#value_marketCap span:first-child');
const displayMarketCap = addCommasToNumber(marketCap.innerText);
marketCap.innerText = displayMarketCap;


