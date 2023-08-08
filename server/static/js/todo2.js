// set todo-add--container width 
const plus = document.querySelector('.todo-plus--btn');
const container = document.querySelector('.main-right--container');
const add_container = document.querySelector('.todo-add--container');
const edit_containers = document.querySelectorAll('.todo-item--edit');
let Add_width = container.clientWidth * 0.8; 
let Edit_width = container.clientWidth * 0.9; 
let Add_right = Add_width + 30;
add_container.style.width = `${Add_width}px`;
add_container.style.left = `80px`;
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
function paintStar(level){
    document.querySelectorAll('.sel-todo-level div').forEach(star => {
        if (star.getAttribute('level') <= level){
            star.classList.add('active');
        } else{
            star.classList.remove('active');
        }
    })
}

plus.addEventListener('click', () => {
    document.querySelector('.todo-plus').classList.toggle('active');
})

const add_todo = async(date_id) => {
    const url = '/main/add_todo/';
    let inputTag = document.querySelector('.todo-add--input input');
    let inputVal = inputTag.value;
    

    const data = { content: inputVal, level: parseInt(level)};
    if (inputVal !== '' && level !== '0'){
        const res = await fetch(url, {
            method: 'POST', 
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(data),
        })
        const {todo_id: todo_id, my_level: my_level, content: content} = await res.json();
        document.querySelector(`.day${date_id}--todo input`).value = '';
        level = '0';
        paintStar('0');
        document.querySelector('.todo-plus').classList.remove('active');
        handleTodoResponse(todo_id, my_level, content);

        
    }else if (inputVal === ''){
        document.querySelector(`.day${date_id}--todo .todo-add--input span`).style.color = '#ff0033';
    }else if (level == '0'){
        document.querySelector(`.day${date_id}--todo .todo-add--level span`).style.color = '#ff0033';
    } 
}

const handleTodoResponse = async(todo_id, level, content) => {
    let paintedLevel = '';
    let emptyLevel = '';
    level = Number(level);
    for(p = 1; p < level + 1; p++){
        paintedLevel += `<div level="${p}" class="active"></div>`;
    }
    for(e = level + 1; e < 6; e++){
        emptyLevel += `<div level="${e}"></div>`;
    }
    
    document.querySelector('.todo-paint').innerHTML += `
    <div class="todo-item todo-item-${todo_id}">
        <div class="todo-checkbox todo-checkbox-${todo_id}" onclick="check_todo(${todo_id})"></div>
        
        <input type="text" 
            class="todo-contents" 
            onclick="edit_todo(${todo_id})"
            value="${content}"
            readonly>
        <div class="todo-level todo-level-${todo_id}">
            ${paintedLevel}
            ${emptyLevel}
        </div>
        
        <div class="todo-item--edit todo-item--edit-${todo_id}">
            <div class="todo-item--date">8월 7일 월요일</div>
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
            <div class="edit-btn--container">
                <div class="todo-edit--delete-btn" onclick="delete_todo(${todo_id})">삭제</div>
                <div class="todo-edit--submit-btn" onclick="update_todo(${todo_id})">완료</div>
            </div>
        </div>
    </div>
    `;
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
    edit_container.classList.toggle('active');
   
    let curr_level = edit_container.querySelector(`.edit-todo-level`).getAttribute('curr-level');
    epaintStar(todo_id, curr_level);

    if(edit_container.classList.contains('active')){
        const content = edit_container.querySelector('input');
        content.focus();
     
        edit_container.querySelectorAll(`.edit-todo-level > div`).forEach(star => {
            star.addEventListener('click', () => {
                
                updated_level = star.getAttribute('level');
                epaintStar(todo_id, updated_level);
                edited_star = true;
                
            }
        )})
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
        const editInput = container.querySelector('input');
        
        if (editContainer.contains(event.target) || event.target.classList.contains('todo-contents')) {
            clickedInsideEditContainer = true;
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

    // ajax
    const url = `/main/update_todo/${todo_id}/`;
    const res = await fetch(url, {
        method: 'POST', 
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({todo_id, curr_level, curr_content}),
    })
    
    const {t_id: t_id, c_level: c_level, c_content: c_content} = await res.json();
    handleUpdateTodoRes(t_id, c_level, c_content);
    edit_container.classList.remove('active');

}

const handleUpdateTodoRes = async(todo_id, level, content) => {
    document.querySelector(`.todo-item-${todo_id} input`).value = content;
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
    console.log(level);
    container.innerHTML = `
            ${paintedLevel}
            ${emptyLevel}
    `;
    edit_container.innerHTML = `
            ${paintedLevel}
            ${emptyLevel}
    `;
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
    const {id: id, d_id: d_id} = await res.json();
    handleDelTodoRes(id, d_id);
}
const handleDelTodoRes = async(todo_id, date_id) => {
    // delete container
    const container = document.querySelector(`.todo-item-${todo_id}`);
    container.remove();
}



// check todo
const check_todo = async(todo_id) => {
    const checkBox = document.querySelector(`.todo-checkbox-${todo_id}`);
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
    
    const {'color': color, 'todo_status': todo_status, 't_id': t_id} = await res.json();
    handleCheckTodoRes(color, todo_status, t_id);
}

function handleCheckTodoRes(color, status, todo_id){
    const checkBox = document.querySelector(`.todo-checkbox-${todo_id}`);
    if (status == 'True'){
        checkBox.classList.add('True');
    } else{
        checkBox.classList.remove('True');
    }
    
}


