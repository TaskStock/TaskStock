
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
const addBtn = document.querySelector('.list__btn');

addBtn.addEventListener('click', () => {
    const newTodo = document.createElement('todo-item');
    document.querySelector('.todo-list-cont').appendChild(newTodo);
    const newTodo_input = newTodo.querySelector('input');
    newTodo_input.focus();
    
})

// blur일 때 input에 아무것도 없으면 지우기
// document.querySelector('.list__btn').addEventListener('click', () => {
//     document.querySelectorAll('todo-item input').forEach(item => {
//         console.log(item);
        
//     })
// })

// set attribute
// document.querySelectorAll('todo-item').forEach(item => {
//     item.addEventListener('change', () => {
//         console.log(item);
//     })
// })

// const todo_container = document.querySelector('.todo-list-cont');
// todo_container.addEventListener('click', (e) => {
//     console.log(e.target.getAttribute('data-status'));
//     if(e.target.classList.contains('todo-checkbox')){
//         // if()
//         const btn = e.target;
//         btn.classList.add('active');
        



//     }else if(e.target.classList.contains('gg-check')){
//         const btn = e.target.parentNode;
//         btn.classList.remove('active');
//     }  
    
// })

function handleCheck(event) {
    event.stopPropagation();
    console.log(event.target);
    let btn = event.currentTarget;
    btn.classList.toggle('active');
}
// const onClickLike = async (id, type) => {
//     const url = '/like_ajax/';
//     const res = await fetch(url, {
//         method: 'POST', 
//         headers: {
//             "Content-Type": "application/x-www-form-urlencoded",
//         },
//         body: JSON.stringify({id: id, type: type}),
//     });
//     const {id: postId, type: button} = await res.json();
//     likeHandleResponse(postId, button);
// }
