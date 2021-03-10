document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#error').style.display = 'none';
  document.querySelector('#email-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  
  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
  document.querySelector('#compose-subject').disabled = false;

  // add addEventListener event to submit button
  document.querySelector('form').addEventListener('submit' , submit_email);

}

function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#email-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#error').style.display = 'none';

  mailbox_rows(mailbox)
  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

}

// submit email
function submit_email(event) {

  //get recipients , subject and body
  const constRecipients = document.querySelector('#compose-recipients').value;
  const constSubject = document.querySelector('#compose-subject').value;
  const constBody = document.querySelector('#compose-body').value;
  
  // post email
  fetch('/emails', {
    method: 'POST',
    body: JSON.stringify({
        recipients: constRecipients,
        subject: constSubject,
        body: constBody
    })
  })
  .then(response => response.json())
  .then(result => {

      // Print result
      console.log(result);
      if(result.error){
        show_error(result.error);
      }else{
        mailbox_rows(result)
        load_mailbox('sent');
      }
  }).catch(error=> {
    console.log(error);  
  });

event.preventDefault();
}

function mailbox_rows(mailbox) {
  
  fetch('/emails/'+ mailbox)
  .then(response => response.json())
  .then(emails => {
  
  emails.forEach(mail => {
    show_mail(mailbox,mail);
  });
  
    // Print emails
  console.log(emails);
  }).catch(error => {
     console.log(error);
  });
}

function show_mail(mailbox,mail) {

  const element = document.createElement('div');
  element.classList.add('mailbox');

  if(!mail.read){
    element.style.background = 'white';
  }else{
    element.style.background = 'gainsboro';
  }
  element.innerHTML =  `<ul>
                            <li>${mail.sender}</li>
                            <li>${mail.subject}</li>
                            <li>${mail.timestamp}</li>
                        </ul>`;

  element.addEventListener('click', function() {
    fetch('/emails/'+mail.id, {
      method: 'PUT',
      body: JSON.stringify({
          read: true
      })
    })
  mail_view(mail);
});

if(mailbox != 'sent')
{
  const archive = document.createElement('div');
  archive.classList.add('archive');
  archive.innerHTML = `<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-archive" viewBox="0 0 16 16">
                      <path d="M0 2a1 1 0 0 1 1-1h14a1 1 0 0 1 1 1v2a1 1 0 0 1-1 1v7.5a2.5 2.5 0 0 1-2.5 2.5h-9A2.5 2.5 0 0 1 1 12.5V5a1 1 0 0 1-1-1V2zm2 3v7.5A1.5 1.5 0 0 0 3.5 14h9a1.5 1.5 0 0 0 1.5-1.5V5H2zm13-3H1v2h14V2zM5 7.5a.5.5 0 0 1 .5-.5h5a.5.5 0 0 1 0 1h-5a.5.5 0 0 1-.5-.5z"/>
                      </svg>`;
  document.querySelector('#emails-view').append(archive);
  archive.addEventListener('click', function() {
    console.log(mail.archived);  
    if (mail.archived){
      fetch('/emails/'+mail.id, {
        method: 'PUT',
        body: JSON.stringify({
          archived: false
        })
      })
    }else{
      fetch('/emails/'+mail.id, {
        method: 'PUT',
        body: JSON.stringify({
          archived: true
        })
      })
    }
    load_mailbox('inbox');
    location.reload();
  });
}
document.querySelector('#emails-view').append(element);
}

function mail_view(mail){

  document.querySelector('#email-reply').addEventListener('click' , () => reply_mail(mail));

  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#error').style.display = 'none';
  document.querySelector('#email-view').style.display = 'block';

  document.querySelector('#email-sender').value = mail.sender;
  document.querySelector('#email-recipients').value = mail.recipients.join(",");
  document.querySelector('#email-subject').value = mail.subject
  document.querySelector('#email-timestamp').value = mail.timestamp
  document.querySelector('#email-body').value = mail.body
  

  
}

function reply_mail(mail) {
  
  compose_email();
  document.querySelector('#compose-recipients').value = mail.sender;
  document.querySelector('#compose-subject').disabled = true;
  var subject = mail.subject;
  if (!subject.toLocaleLowerCase().startsWith("re:")){
      subject = "Re: ".concat(subject);
  }
  document.querySelector('#compose-subject').value =subject;
  document.querySelector('#compose-body').value = "\r\n" + "\r\n" + "\r\n" + "\r\n" + "On " + mail.timestamp +  " " + mail.sender +  " " + "wrote: " + "\r\n" + mail.body;
}

function show_error(error){

  const element_error = document.querySelector('#error')
  element_error.innerHTML = `<h6> <span> Error</span> </h6> <ul> <li>${error}</li></ul>`;
  element_error.classList.add('alert');
  element_error.classList.add('alert-danger');
  document.querySelector('#error').style.display = 'block';

}

