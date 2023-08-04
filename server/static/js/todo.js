
// // const handleBlur = () => {
// //     const todoContent = document.querySelector('.todo-content');
// //     if (!todoContent.value.trim()) {
// //         this.parentNode.remove();
// //     }
// // }
// // const todo_items = document.querySelectorAll('todo-item');

// // custom element - todo
// class TodoItem extends HTMLElement {
//     constructor() {
//         super();
//     }
//     connectedCallback() {
//         this.render();
//         const todoContent = document.querySelector('.todo-content');
//         todoContent.addEventListener('blur', this.handleBlur);
//     }
//     static get observedAttributes() {
//         return ['content', 'level', 'status', 'date'];
//     }
//     attributeChangedCallback(atrb, oldV, newV) {
//         if (atrb === 'content'){
//             this.render();
//             // ajax 값 보내기 
//         }
//     }
    
//     render(){
//         // innerHTML 구성

//         const todo_checkbox = document.createElement('div');
//         todo_checkbox.classList.add('todo-checkbox');
//         // todo_checkbox.onclick = addTodoHandler;

//         const todo_ci = document.createElement('i');
//         todo_ci.classList.add('gg-check');
//         todo_checkbox.appendChild(todo_ci);

//         const todo_content = document.createElement('input');
//         todo_content.classList.add('todo-content');
//         todo_content.type = "text";
        
//         const todo_more = document.createElement('div');
//         todo_more.classList.add('todo-more');

//         const todo_i = document.createElement('i');
//         todo_i.classList.add('gg-more-alt');

//         todo_more.appendChild(todo_i);

//         this.appendChild(todo_checkbox);
//         this.appendChild(todo_content);
//         this.appendChild(todo_more);
//         this.classList.add('todo-item');
       
        
        
        
//         // const todo = this.getAttribute('content');
//         // todo_content.value = `${todo}`;


//         // 임시 remove 버튼
//         const removeBtn = this.querySelector('.todo-more');
//         removeBtn.addEventListener('click', () => {
//             this.remove();
//         });

//         // checked or unchecked
//         const checkBox = this.querySelector('.todo-checkbox');
//         checkBox.addEventListener('click', () => {
//             checkBox.classList.toggle('active');
//         })
//     }
// }
// customElements.define("todo-item", TodoItem);




// add todo
const handleAdd = (date_id) => {
    document.querySelector('.todo-list-cont').innerHTML +=  `
    <div class="todo-item day${date_id}">
        <div class="todo-checkbox new-todo-checkbox" data-status="False" onclick="handleCheck(event)">
            <i class="gg-check"></i>
        </div>
        <input type="text" class="todo-content" onblur="handleTodo()">
        <div class="todo-more">
            <i class="gg-erase"></i>
        </div>
    </div>
    `;
    let inputTag = document.querySelector('.todo-item:last-child input');
    inputTag.focus();

}




const handleTodo = async() => {
    const url = '/main/add_todo/';
    let inputTag = document.querySelector('.todo-item:last-child input');
    let inputVal = inputTag.value;

    const data = { content: inputVal };
    if (inputVal !== ''){
        const res = await fetch(url, {
            method: 'POST', 
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(data),
        })
        const {date_id: date_id, todo_id: todo_id, content: content} = await res.json();
        handleTodoResponse(date_id, todo_id, content);
        document.querySelector('.new-todo-checkbox').parentNode.remove();
    }else{
        inputTag.parentNode.remove();
    }
}

const handleTodoResponse = async(date_id, todo_id, content) => {
    document.querySelector('.todo-list-cont').innerHTML +=  `
    <div class="todo-item day${date_id}-todo${todo_id}">
        <div class="todo-checkbox" data-status="False" onclick="handleCheck(event)">
            <i class="gg-check"></i>
        </div>
        <input type="text" class="todo-content" value="${content}">
        <div class="todo-more">
            <i class="gg-erase"></i>
        </div>
    </div>
    `;
}   





function handleCheck(event) {
    event.stopPropagation();
    let btn = event.currentTarget;
    btn.classList.toggle('active');
    console.log(event.target);

}

