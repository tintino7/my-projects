document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);
  
  document.querySelector('#compose-form').onsubmit = sent_email;

  document.querySelector('#archive').onclick = archive;
  document.querySelector('#unarchive').onclick = un_archive;
  document.querySelector('#reply').onclick =reply;
  
  // By default, load the inbox
  load_mailbox('inbox');
});




function compose_email(purpose) {


  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#mail_view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';
  
  
  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
  
}




function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#mail_view').style.display = 'none';
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;
  if (mailbox === 'inbox')
  {
    load_page('inbox')
  }
  else if (mailbox === 'sent')
  {
    load_page('sent')
  }
  else if (mailbox === 'archive')
  {
    load_page('archive')
  }
}



// Sent email and redirect to sent
function sent_email(){

  fetch('/emails', {
    method: 'POST',
    body: JSON.stringify({
        // Get value from form,s child elements
        recipients: document.querySelector('#compose-recipients').value,
        subject: document.querySelector('#compose-subject').value ,
        body: document.querySelector('#compose-body').value
    })
  })
  .then(response => response.json())
  .then(result => { 
      console.log(result);

      // Inside the fetch because it,s async outside fetch is fail
      load_mailbox('sent');
      
  });
  // Avoid submitting form to server
  return false
  
}



// Load contents of respective page
function load_page(page_name){
  fetch(`/emails/${page_name}`)
  .then(response => response.json())
  .then(emails => {
      // Print emails
      console.log(emails);
      emails.forEach(email => {

        // Create element add class name
        const div = document.createElement('div');
        div.className = 'email-div';
        div.setAttribute('data-id', email.id);
        const sender = document.createElement('h6');
        sender.className = 'email-sender';
        sender.innerHTML = email.sender;
        const subject = document.createElement('h6');
        subject.className = 'email-subject';
        subject.innerHTML = email.subject;
        const time_stamp = document.createElement('h6');
        time_stamp.className = 'email-timestamp';
        time_stamp.innerHTML = email.timestamp;


        if (page_name === 'inbox')
        {
          // mail not readed
          if (email.read === true)
          {
            div.className = 'email-div-unread'
          }
          
        }

        // Append all child elements to parent div
        div.append(sender, subject,time_stamp)

        // Append div element into emails-view
        document.querySelector('#emails-view').append(div)

      });

        
  });
}





// clicking the mail div 
document.addEventListener('click', event=>{
    
    const element = event.target;

    if (element.className === 'email-div' || element.className === 'email-div-unread')
    {
      // show mail div and hide other divs
      document.querySelector('#emails-view').style.display = 'none';
      document.querySelector('#compose-view').style.display = 'none';
      document.querySelector('#mail_view').style.display = 'block';
      
      const id = parseInt(element.dataset.id);
      
      fetch(`/emails/${id}`)
      .then(response => response.json())
      .then(email => {
      // Print email
      console.log(email);
      

      // Add elements inside mail div 
      document.querySelector('#from').innerHTML =  `<b>From:</b> ${email.sender}`;
      document.querySelector('#to').innerHTML = `<b>To:</b> ${email.recipients}`;
      document.querySelector('#subject').innerHTML = `<b>Subject:</b> ${email.subject}`;
      document.querySelector('#timestamp').innerHTML = `<b>Time stamp:</b> ${email.timestamp}`;

      document.querySelector('#reply').setAttribute('data-id',email.id);
      document.querySelector('#archive').setAttribute('data-id',email.id);
      document.querySelector('#unarchive').setAttribute('data-id', email.id);
      // mail not archived
      if (email.archived === true)
      {
        document.querySelector('#archive').style.display = 'none';
        document.querySelector('#unarchive').style.display ='block';
      }
      // mail archived
      else
      {
        document.querySelector('#archive').style.display = 'block';
        document.querySelector('#unarchive').style.display ='none';
      }

      // for emails under send option hide archive and unarchive button
      if (email.sender === document.querySelector('h2').innerHTML)
      {
        document.querySelector('#archive').style.display = 'none';
        document.querySelector('#unarchive').style.display ='none';
      }
      
      // Add body of the mail inside mail div's div with id of body
      document.querySelector('#body').innerHTML = email.body;

      // update mail as readed
      fetch(`/emails/${id}`, {
        method: 'PUT',
        body: JSON.stringify({
            read: true
        })
      })
    });

        
      }
  })



  // To archive a email
  function archive(){
    const id = parseInt(this.dataset.id);
    // Put request to archive a mail
    fetch(`/emails/${id}`, {
      method: 'PUT',
      body: JSON.stringify({
          archived: true
      })
    })
    .then(response => response.json)
    .then(result =>{
      // Redirect to inbox view
      load_mailbox('inbox');
    })
  }


  // To unarchive a email
  function un_archive(){
    const id = parseInt(this.dataset.id);
    
    // Put request to archive a mail
    fetch(`/emails/${id}`, {
      method: 'PUT',
      body: JSON.stringify({
          archived: false
      })
    })
    .then(response => response.json)
    .then(result =>{
      // Redirect to inbox view
      load_mailbox('inbox');
    })
  }



  // reply for email
  function reply(){
   const id = parseInt(document.querySelector('#reply').dataset.id);
   fetch(`/emails/${id}`)
      .then(response => response.json())
      .then(email => {

      // Print email
      console.log(email);
      
      // Show compose view and hide other views
      document.querySelector('#emails-view').style.display = 'none';
      document.querySelector('#mail_view').style.display = 'none';
      document.querySelector('#compose-view').style.display = 'block';
      

      // Prepopulate all the fields
      document.querySelector('#compose-recipients').value = email.sender;

      // 'Re: ' already exist
      if (email.subject.includes('Re: '))
      {
        document.querySelector('#compose-subject').value = `${email.subject}`;
      }
      // 'Re: ' not exist
      else
      {
        document.querySelector('#compose-subject').value = `Re: ${email.subject}`;
      }
      
      // Prepopulate the body field
      document.querySelector('#compose-body').value = `On ${email.timestamp} ${email.sender} wrote: ${email.body}\n`;
      });
  }