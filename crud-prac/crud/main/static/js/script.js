
let getButton = document.getElementById("getSubmit");
getButton.addEventListener('click', () => {
    let id = document.getElementById('idField').value;
    fetch(`/users?id=${id}`)
        .then((response) => {
            if (response != 200) document.getElementById('resBody').innerHTML = response.status;
            return response.json()
        })
        .then((data) => {
            document.getElementById('resBody').innerHTML = JSON.stringify(data, null, '\t');
        });
});

let postButton = document.getElementById("postSubmit");
postButton.addEventListener('click', () => {
    let form = document.getElementById('post-form-object');
    fetch(`/users`, {
        method: 'POST',
        body: JSON.stringify(Object.fromEntries(new FormData(form))),
    }).then((response) => {
        if (response.status != 200) document.getElementById('resBody').innerHTML = response.status;
        return response.json()
    }).then((data) => {
        form.reset();
        document.getElementById('resBody').innerHTML = JSON.stringify(data);
    });
});

let putButton = document.getElementById("putSubmit");
putButton.addEventListener('click', () => {
    let form = document.getElementById('put-form-object');
    fetch(`/users`, {
        method: 'PUT',
        body: JSON.stringify(Object.fromEntries(new FormData(form))),
    }).then((response) => {
        if (response != 200) document.getElementById('resBody').innerHTML = response.status;
        return response.json()
    }).then((data) => {
        form.reset();
        document.getElementById('resBody').innerHTML = JSON.stringify(data);
    });
});

let confirmDeleteButton = document.getElementById("confirmDeleteSubmit");
confirmDeleteButton.addEventListener('click', () => {
    let modal = document.getElementById("deleteConfirmModal");
    let deleteField = document.getElementById('delete-field');
    if (deleteField.value) modal.style.display = 'block';
});

let cancelDeleteSubmit = document.getElementById("cancelDeleteSubmit");
cancelDeleteSubmit.addEventListener('click', () => {
    let modal = document.getElementById("deleteConfirmModal");
    modal.style.display = 'none';
});

let deleteButton = document.getElementById("deleteSubmit");
deleteButton.addEventListener('click', () => {
    let modal = document.getElementById("deleteConfirmModal");
    modal.style.display = 'none';
    let form = document.getElementById('delete-form-object');
    fetch(`/users`, {
        method: 'DELETE',
        body: JSON.stringify(Object.fromEntries(new FormData(form))),
    }).then((response) => {
        form.reset();
        document.getElementById('resBody').innerHTML = response.status
    });
});


let crudButtons = document.getElementsByClassName('request-btn');
for (var i = 0; i < crudButtons.length; i++) {
    crudButtons[i].addEventListener('click', function () {
        document.querySelectorAll('.request-form').forEach(element => {
            element.style.display = 'none';
        });
        let selectedForm = document.getElementById(`${this.id}-form`);
        selectedForm.style.display = 'block';
    });
}

(function () {
    fetchTable(1);
})();

function fetchTable(page) {
    fetch(`users?page=${page}`)
        .then((response) => {
            return response.json()
        })
        .then((data) => {
            let tableBody = document.getElementById('tableBody');
            tableBody.innerHTML = '';
            data.forEach(each => {
                let tr = document.createElement('tr');
                let firstName = document.createElement('td');
                firstName.innerHTML = each['first_name'];
                let lastName = document.createElement('td');
                lastName.innerHTML = each['last_name'];
                let email = document.createElement('td');
                email.innerHTML = each['email'];
                let username = document.createElement('td');
                username.innerHTML = each['username'];
                tr.appendChild(firstName);
                tr.appendChild(lastName);
                tr.appendChild(username);
                tr.appendChild(email);
                tableBody.appendChild(tr);
            });
        });
}

let paginateButton = document.getElementById('paginate');
paginateButton.addEventListener('click', function () {
    let page = document.getElementById('page').value;
    fetchTable(page);
});