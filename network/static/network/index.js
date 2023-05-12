




// Cliking like button
document.querySelectorAll('.like').forEach(icon =>{
    icon.onclick = function(){
        let status;
        const post_id = icon.dataset.post_id;

        // want to unlike
        if (icon.id === 'like')
        {
            icon.src = 'static/heart1.png'
            icon.id = 'unlike'
            status = 'unlike'
            
        }
        // want to like
        else if (icon.id === 'unlike')
        {
            icon.src = 'static/heart.png'
            icon.id = 'like'
            status = 'like'    
        }
        
        // fetch to like url
        fetch('/like', {
            method:'PUT',
            body: JSON.stringify({
                action: status,
                post_id: post_id
            })    
        })
        .then(responce => responce.json())
        .then(result =>{
            console.log(result)
            // select respective like count div
            const like_countDiv = document.querySelector(`#like-count${post_id}`)
            let like_count = parseInt(like_countDiv.innerHTML)

            // unlike means substract 1
            if (status === 'unlike')
            {
                like_count--
                like_countDiv.innerHTML = like_count
            }
            // like means add 1
            else if(status === 'like')
            {
                like_count++
                like_countDiv.innerHTML = like_count
            }
        })
    }
})








    

// clicking the edit button
document.querySelectorAll('#edit').forEach(edit =>{

    edit.onclick = function(){
        const parent = edit.parentElement;
        const grant_parent = parent.parentElement;
        grant_parent.querySelector('#content').style.display = 'none';
        grant_parent.querySelector('#content-edit').style.display = 'block';
    }
})


// clicking the cancel button
document.querySelectorAll('#cancel').forEach(cancel =>{
    cancel.onclick = function(){
        
        const parent = cancel.parentElement;
        const grant_parent = parent.parentElement;
        const content = grant_parent.querySelector('#content');
        const content_edit = grant_parent.querySelector('#content-edit');
        
        // hide content_edit and show content
        if (content.style.display === 'none' && content_edit.style.display === 'block')
        {
            content.style.display = 'block';
            content_edit.style.display = 'none'
        } 
    }
})


document.querySelectorAll('#edit_form').forEach(edit_form =>{
    edit_form.onsubmit = function(){
        // get id and content
        const post_id = parseInt(edit_form.querySelector('#post_id').value);
        const content = edit_form.querySelector('#edited_content').value;
        console.log(post_id,content)
        
        fetch('/edit',{
            method:'PUT',
            body: JSON.stringify({
                post_id: post_id,
                content: content
            })
        })
        .then(responce =>responce.json())
        .then(result =>{
            console.log(result)
            const parent = edit_form.parentElement;
            const grant = parent.parentElement;
            const content_div = grant.querySelector('#content');
            const content_edit_div = grant.querySelector('#content-edit');
            

            if (content_div.style.display === 'none' && content_edit_div.style.display === 'block')
            {
                // status is success
                if (result.status === 'success')
                {
                    content_div.querySelector('p').innerHTML = content;
                }
                // status is unsuccess
                else
                {
                    alert('Something went wrong try again. Try to reload the page')
                }
                
                content_div.style.display = 'block';
                content_edit_div.style.display = 'none';
            }
              
        })
        return false
    }
})