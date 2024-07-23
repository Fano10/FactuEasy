
function main(){
    let form = document.getElementById('form')
    form.addEventListener('submit', (e) =>{
        e.preventDefault();
        url = '/authentification';
        urlRedict = '/allBills'
        let username = document.getElementById('name');
        let password = document.getElementById('password');
        let formData = {
            "username": username.value,
            "password": password.value
        }
        let data = JSON.stringify(formData);
        fetch(url,{
            method:'POST',
            headers: {'Content-Type' : 'application/json'},
            credentials: 'include',
            body: data
        })
        .then(response => {
            let data = response.json()
            let statusCode = response.status;
            let cookies = document.cookie;
            if(statusCode ===200){
                window.location.href = urlRedict;
            }
            else {
                document.getElementById('erreur').innerHTML = 'Wrong username or password. Please try again';
            }

        })
        .catch(error => {
            console.error('Fetch error:',error);
        })
    })
}

window.onload = main;