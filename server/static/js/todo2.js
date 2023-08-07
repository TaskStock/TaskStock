// set todo-add--container width 
const plus = document.querySelector('.todo-plus--btn');
const container = document.querySelector('.main-right--container');
const add_container = document.querySelector('.todo-add--container');

let Add_width = container.clientWidth * 0.8; 
let Add_right = Add_width + 30;
add_container.style.width = `${Add_width}px`;
add_container.style.left = `80px`;


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
        const {date_id: date_id, todo_id: todo_id, my_level: my_level, content: content} = await res.json();
        document.querySelector(`.day${date_id}--todo input`).value = '';
        level = '0';
        paintStar('0');
        document.querySelector('.todo-plus').classList.remove('active');
        handleTodoResponse(date_id, todo_id, my_level, content);

        
    }else if (inputVal === ''){
        document.querySelector(`.day${date_id}--todo .todo-add--input span`).style.color = '#ff0033';
    }else if (level == '0'){
        document.querySelector(`.day${date_id}--todo .todo-add--level span`).style.color = '#ff0033';
    } 
}

const handleTodoResponse = async(date_id, todo_id, level, content) => {
    document.querySelector('.todo-item').innerHTML += ``;

}





// edit todo
let updated_level = 0;
let edited_star = false;

const edit_todo = (todo_id) => {
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

    // level 어떡하지........

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

// check todo
const check_todo = (todo_id) => {
    document.querySelector(`.todo-checkbox-${todo_id}`).classList.toggle('done');
}