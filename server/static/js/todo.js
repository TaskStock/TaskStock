let level = '0';
const level_stars = document.querySelectorAll('.sel-todo-level i');
level_stars.forEach(star => {
    star.addEventListener('click', () => {
        level = star.getAttribute('level');
        paintStar(level);
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

const handleAddTodo = async(date_id) => {
    const url = '/main/add_todo/';
    let inputTag = document.querySelector('.list__input-cont input');
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
        const {date_id: date_id, todo_id: todo_id, my_level: my_level, content: content} = await res.json();
        handleTodoResponse(date_id, todo_id, my_level, content);
        document.querySelector(`.day${date_id}--todo`).value = '';
        level = '0';
        paintStar('0');
    }
}

const handleTodoResponse = async(date_id, todo_id, level, content) => {
    document.querySelector('.todo-list-cont').innerHTML +=  `
    <div class="todo-item day${date_id}-todo${todo_id}">
        <div class="todo-checkbox" data-status="todo.goal_check" onclick="handleCheck(event)">
            <i class="gg-check"></i>
        </div>
        <div class="todo-input-cont">
            <input type="text" class="todo-content" value="${content}" readonly>
            <div class="todo-level todo-level-${todo_id}">
                <i class="fa-solid fa-star"></i>
                <div>${level}</div>
            </div>
        </div>
        <div class="todo-edit todo-edit-${todo_id}">
            <i class="gg-edit-markup"></i>
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
function handleCheck(event) {
    event.stopPropagation();
    let btn = event.currentTarget;
    btn.classList.toggle('active');
    console.log(event.target);

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
// more
function handleMore(todo_id){
    const more_container = document.querySelector(`.todo-edit-${todo_id}`);
    const more_btn = document.querySelector(`.todo-more-${todo_id}`);
    const more_btn_i = more_btn.querySelector('i');
    const prev_level = document.querySelector(`.todo-level-${todo_id}`);
    let curr_level = more_container.querySelector('.edit-todo-level').getAttribute('curr-level');
    epaintStar(todo_id, curr_level);
    if (more_btn.classList.contains('active')){
        more_container.style.display = 'none';
        more_btn.classList.remove('active');
        more_btn_i.classList.remove('gg-check');
        more_btn_i.classList.add('gg-more-alt');
        prev_level.style.display = 'flex';

        
    }else{
        more_container.style.display = 'flex';
        more_btn.classList.add('active');
        more_btn_i.classList.remove('gg-more-alt');
        more_btn_i.classList.add('gg-check');
        prev_level.style.display = 'none';

        

        // level
        const elevel_stars = more_container.querySelectorAll('.edit-todo-level i');
        elevel_stars.forEach(star => {
            star.addEventListener('click', () => {
                level = star.getAttribute('level');
                epaintStar(todo_id, level);
            }
        )})

    }
}