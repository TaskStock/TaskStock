// custom element - todo
class cTodo extends HTMLElement {
    
    connectedCallback() {
        let todo_container = document.createElement('div');
        todo_container.classList.add('list__list');
        
        todo_container.innerHTML = `
            <div class="todo-checkbox" onclick="addTodoHandler()"><i class="gg-check"></i></div>
            <input type="text" class="todo-content" autofocus>
            <div class="todo-more"><i class="gg-more-alt"></i></div>
        `
        this.appendChild(todo_container);
        
    }
    static get observedAttributes() {
        return ['value']
    }
    attributeChangedCallback(attrName, oldVal, newVal) {
        this[attrName] = newVal;
    }
}

customElements.define("to-do", cTodo);



// add todo
addBtn = document.querySelector('.list__btn');
addBtn.addEventListener('click', () => {
    const newTodo = document.createElement('to-do');
    document.querySelector('.list__list-cont').appendChild(newTodo);

    const newTodo_input = document.querySelector('to-do input');
    console.log(newTodo_input);
    
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


