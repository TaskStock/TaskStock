// custom element - todo
class cTodo extends HTMLElement {
    connectedCallback() {
        const todo_container = document.createElement('div');
        todo_container.classList.add('list__list');

        const todo_checkbox = document.createElement('div');
        todo_checkbox.classList.add('todo-checkbox');
        
        const todo_content = document.createElement('input');
        todo_content.classList.add('todo-content');
        todo_content.type = "text";
        
        const todo_more = document.createElement('div');
        todo_more.classList.add('todo-more');

        const todo_i = document.createElement('i');
        todo_i.classList.add('gg-more-alt');

        todo_more.appendChild(todo_i);

        todo_container.appendChild(todo_checkbox);
        todo_container.appendChild(todo_content);
        todo_container.appendChild(todo_more);

        this.appendChild(todo_container);
        
        // set attribute (content, level, status)
        this.setAttribute('content', `${todo_content.value}`);
        this.setAttribute('level', 1);
        this.setAttribute('status', 'unchecked');
    }
    static get observedAttributes() {
        return ['content', 'level', 'status'];
    }
    attributeChangedCallback() {
        todo_content = this.querySelector('.todo-content');
        console.log(todo_content);

        this['content'] = todo_content.value;
    }
}

customElements.define("to-do", cTodo);



// add todo
addBtn = document.querySelector('.list__btn');
addBtn.addEventListener('click', () => {
    const newTodo = document.createElement('to-do');
    document.querySelector('.list__list-cont').appendChild(newTodo);
    const newTodo_input = newTodo.querySelector('input');
    newTodo_input.focus();


    
})

// 

const addTodoHandler = () => {
    checkBoxes = document.querySelectorAll('.todo-checkbox');

    checkBoxes.forEach((checkBox) => {
        checkBox.addEventListener('click', () => {
            checkBox.classList.toggle('active');
            console.log('clicked');
            console.log(document.querySelector('to-do input').value);
        })
    })
}


