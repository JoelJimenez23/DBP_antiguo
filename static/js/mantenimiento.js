const pendingForms = new WeakMap()

createUser()

function createUser(){
    const formCreateUserId = document.querySelector('#formCreateUserId',)
    formCreateUserId.addEventListener('submit', handlingSubmitUser)
}
function handlingSubmitUser(event){
    event.preventDefault()
    event.stopPropagation()

    const formCreateUser = event.currentTarget
    const previousController = pendingForms.get(formCreateUser)

    if(previousController){previousController.abort()}

    const controller = new AbortController()
    pendingForms.set(formCreateUser,controller)
    console.log('formCreateEmployee: ', formCreateEmployee)


    const formData = new FormData(formCreateUser)

    fetch('/register-user',{
        method: 'POST',body: formData,signal: controller.signal
    })
    .then((response)=> response.json())
        .then((responseJson)=>{
            if(responseJson.succes){
                const succesUserMessage = document.getElementById('successUserMessage',)
                succesUserMessage.style.display = 'block';
                succesUserMessage.innerHTML = responseJson.message;

                setTimeout(()=>{
                    formCreateUser.reset()
                    succesUserMessage.style.display = 'none';
                },3000)
            }
            else{
                const errorUserMessage = document.getElementById('errorUserMessage',)
                errorUserMessage.style.display = 'block';

                setTimeout(() => {
                    formCreateUser.reset()
                    errorUserMessage.style.display = 'none';
                },3000)
            }
    })
}

function handlingSubmitUser(event){}
