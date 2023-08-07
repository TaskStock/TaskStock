let level = '0';
const level_stars = document.querySelectorAll('.sel-todo-level i');
level_stars.forEach(star => {
    star.addEventListener('click', () => {
        level = star.getAttribute('level');
        paintStar(level);
        document.querySelector('.todo-error').style.display = 'none';
        document.querySelector('.todo-error').style.display = 'none';
    }
)})
function paintStar(level){
    document.querySelectorAll('.sel-todo-level i').forEach(star => {
        if (star.getAttribute('level') <= level){
            star.classList.remove('fa-regular');
            star.classList.add('fa-solid');
        } else{
            star.classList.remove('fa-solid');
            star.classList.add('fa-regular');
        }
    })
}
function epaintStar(todo_id, level){
    const editCon = document.querySelector(`.todo-edit-${todo_id}`);
    editCon.querySelectorAll('.edit-todo-level i').forEach(star => {
        if (star.getAttribute('level') <= level){
            star.classList.remove('fa-regular');
            star.classList.add('fa-solid');
        } else{
            star.classList.remove('fa-solid');
            star.classList.add('fa-regular');
        }
    })
}
const handleAddTodo = async(date_id) => {
    const url = '/main/add_todo/';
    let inputTag = document.querySelector('.list__input-cont input');
    let inputVal = inputTag.value;
    const error = document.querySelector('.todo-error');

    const data = { content: inputVal, level: parseInt(level)};
    if (inputVal !== '' && level !== '0'){
        const res = await fetch(url, {
            method: 'POST', 
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(data),
        })
        const {date_id: date_id, todo_id: todo_id, my_level: my_level, content: content} = await res.json();
        handleTodoResponse(date_id, todo_id, my_level, content);
        document.querySelector(`.day${date_id}--todo`).value = '';
        level = '0';
        paintStar('0');
        error.style.display = 'none';
    }else if (inputVal === ''){
        error.style.display = 'block';
        error.innerHTML = '할 일을 입력하세요.';
    }else if (level == '0'){
        error.style.display = 'block';
        error.innerHTML = '난이도를 선택하세요.';
    } 
}

const handleTodoResponse = async(date_id, todo_id, level, content) => {
    document.querySelector('.todo-list-cont').innerHTML +=  `
    <div class="todo-item day${date_id}-todo${todo_id}">
        <div class="todo-checkbox todo-checkbox-${todo_id}" data-status="todo.goal_check" onclick="handleCheck(event)">
            <i class="gg-check"></i>
        </div>
        <div class="todo-input-cont todo-input-cont-${todo_id}">
            <input type="text" 
                   class="todo-content" 
                   value="${content}" 
                   onkeypress="if(event.keyCode==13) {handleMore(${todo_id})}" 
                   readonly>
            <div class="todo-level todo-level-${todo_id}">
                <i class="fa-solid fa-star"></i>
                <div>${level}</div>
            </div>
        </div>
        <div class="todo-edit todo-edit-${todo_id}">
            <div class="edit-todo-level" curr-level="${level}">
                <i class="fa-regular fa-star" level="1"></i>
                <i class="fa-regular fa-star" level="2"></i>
                <i class="fa-regular fa-star" level="3"></i>
                <i class="fa-regular fa-star" level="4"></i>
                <i class="fa-regular fa-star" level="5"></i>
            </div>
            <i class="gg-edit-markup" onclick="handleEditInput(${todo_id})"></i>
            <div class="edit-todo-level" curr-level="${level}">
                <i class="fa-regular fa-star" level="1"></i>
                <i class="fa-regular fa-star" level="2"></i>
                <i class="fa-regular fa-star" level="3"></i>
                <i class="fa-regular fa-star" level="4"></i>
                <i class="fa-regular fa-star" level="5"></i>
            </div>
            <i class="gg-edit-markup" onclick="handleEditInput(${todo_id})"></i>
            <i class="gg-trash" onclick="handleDeleteTodo(${todo_id})"></i>
        </div>
        <div class="todo-more todo-more-${todo_id}" onclick="handleMore(${todo_id})">
            <i class="gg-more-alt"></i>
        </div>
    </div>
    `;

}   

// delete todo
const handleDeleteTodo = async(todo_id) => {
    const url = `/main/delete_todo/${todo_id}/`;
    const res = await fetch(url, {
        method: 'POST', 
        headers: {
            "Content-Type": "application/x-www-form-urlencoded",
        },
        body: JSON.stringify({todo_id}),
    })
    const {id: id, d_id: d_id} = await res.json();
    handleDelTodoRes(id, d_id);
}

const handleDelTodoRes = async(todo_id, date_id) => {
    // delete container
    const container = document.querySelector(`.day${date_id}-todo${todo_id}`);
    container.remove();
}


// check
const handleCheck = async(todo_id) => {
    let status = 'unchecked';
    let btn = document.querySelector(`.todo-checkbox-${todo_id}`);
    btn.classList.toggle('active');

    if(btn.classList.contains('active')){
        status = 'checked';
        console.log(status);
        // ajax
        const url = `/main/check_todo/${todo_id}/`;
        const res = await fetch(url, {
            method: 'POST', 
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({todo_id, status}),
        })
        
        const {t_id: t_id, c_level: c_level, c_content: c_content} = await res.json();
        handleUpdateTodoRes(t_id, c_level, c_content);

    }else{
        status = 'unchecked';
        console.log(status);
    }
    

}


// more
let updated_level = 0;
let edited_star = false;
const handleMore = async(todo_id) => {
    const more_container = document.querySelector(`.todo-edit-${todo_id}`);
    const more_btn = document.querySelector(`.todo-more-${todo_id}`);
    const more_btn_i = more_btn.querySelector('i');
    const prev_level = document.querySelector(`.todo-level-${todo_id}`);
    let curr_level = more_container.querySelector('.edit-todo-level').getAttribute('curr-level');
    const elevel_stars = more_container.querySelectorAll('.edit-todo-level i');
    epaintStar(todo_id, curr_level);
    
    const content_container = document.querySelector(`.todo-input-cont-${todo_id}`);
    const content = content_container.querySelector(`input`);
    

    if (more_btn.classList.contains('active')){
        more_container.style.display = 'none';
        more_btn.classList.remove('active');
        more_btn_i.classList.remove('gg-check');
        more_btn_i.classList.add('gg-more-alt');
        prev_level.style.display = 'flex';
        content.readOnly = true;
        content.blur();
        // content_container.style.borderBottom = 'none';
        if (edited_star === true){
            curr_level = updated_level
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

        
    }else{
        more_container.style.display = 'flex';
        more_btn.classList.add('active');
        more_btn_i.classList.remove('gg-more-alt');
        more_btn_i.classList.add('gg-check');
        prev_level.style.display = 'none';

        

        // level
        elevel_stars.forEach(star => {
            star.addEventListener('click', () => {
                updated_level = star.getAttribute('level');
                epaintStar(todo_id, updated_level);
                edited_star = true;
                
            }
        )})
    }
}

const handleUpdateTodoRes = async(todo_id, level, content) => {
    const update_container = document.querySelector(`.todo-edit-${todo_id}`);
    const level_container = update_container.querySelector('.edit-todo-level')
    const content_container = document.querySelector(`.todo-input-cont-${todo_id}`);
    
    level_container.setAttribute('curr-level', level);
    document.querySelector(`.todo-level-${todo_id} div`).innerHTML = `${level}`;
    content_container.querySelector('input').value = content;
}

function handleEditInput(todo_id){
    const container =  document.querySelector(`.todo-input-cont-${todo_id}`); 
    const content = container.querySelector(`input`);
    content.readOnly = false;
    content.focus();
    // container.style.borderBottom = '2px solid var(—green_400)';

    // 커서 뒤로
    let prev_value = content.value;
    content.value = ''
    content.value = prev_value;
    // 


}
