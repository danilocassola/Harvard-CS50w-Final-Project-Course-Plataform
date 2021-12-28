// csrftoken
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getCookie('csrftoken');


function done_lesson(lesson_id) {
    const request = new Request(
        `/done`,
        {headers: {'X-CSRFToken': csrftoken}}
    );

    fetch(request, {
        method: "PUT",
        body: JSON.stringify({
            lesson: lesson_id
        })
    })
    .then(response => response.json())
    .then(data => {
        // Check if the lesson is done
        if (data.lesson_done === "True") {
            document.querySelector(`#mark_${lesson_id}`).className = "ms-2 bi bi-check-circle-fill";
            document.querySelector(`#mark_${lesson_id}`).style.color = "green";
            document.querySelector(`#text_done_${lesson_id}`).innerHTML = "Mark as undone";
            // Menu
            document.querySelector(`#tx_done_menu_${lesson_id}`).className = "mx-1 bi bi-check-square-fill";
            document.querySelector(`#tx_done_menu_${lesson_id}`).style.color = "green";
        } 
        else {
            document.querySelector(`#mark_${lesson_id}`).className = "ms-2 bi bi-check-circle";
            document.querySelector(`#mark_${lesson_id}`).style.color = "gray";
            document.querySelector(`#text_done_${lesson_id}`).innerHTML = "Mark as done";
            // Menu
            document.querySelector(`#tx_done_menu_${lesson_id}`).className = "mx-1 bi bi-check-square";
            document.querySelector(`#tx_done_menu_${lesson_id}`).style.color = "gray";
        }

        // Check if the module is done
        if (data.done_module == true) {
            document.querySelector(`#mod_done_${data.module_id}`).className = "me-2 bi bi-check-circle-fill";
            document.querySelector(`#mod_done_${data.module_id}`).style.color = "green";
        }
        else {
            document.querySelector(`#mod_done_${data.module_id}`).className = "me-2 bi bi-check-circle";
            document.querySelector(`#mod_done_${data.module_id}`).style.color = "gray";
        }

        // Course Progress
        document.querySelector("#course_progress").innerHTML = data.progress_course + "%";
        document.querySelector("#course_progress_bar").style.width = data.progress_course + "%";
        document.querySelector("#course_progress_bar").ariaValueNow = data.progress_course;
    }) 
    .catch((error) => {
        console.error("Error: ", error);
    });
    return false;
}


function get_modules(course_id) {

    const request = new Request(
        `/modules_api/${course_id}`,
        {headers: {'X-CSRFToken': csrftoken}}
    );

    fetch(request) 
    .then(response => response.json())
    .then(modules => {
        document.getElementById("module").innerHTML = "";
        document.getElementById("module").innerHTML = '<option value="" selected disabled>-----</option>';

        modules.forEach(mod => load_mod(mod));

        function load_mod(mod) {
            var x = document.getElementById("module");
            var option = document.createElement("option");
            option.text = mod.title ;
            option.value = mod.id;
            x.add(option);
        };

    })
    .catch(error => {
        console.log("error: ", error);
    });
}

