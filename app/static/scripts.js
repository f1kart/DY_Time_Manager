function calculate_and_display_progress(truck) {
  let totalStandardTime = 0;
  let totalActualTime = 0;

  for (const task of truck.tasks) {
    totalStandardTime += task.standard_time; // Assuming 'standard_time' is in a time interval format
    totalActualTime += task.total_time; // Assuming 'total_time' is already calculated
  }

  let progressPercentage = 0;
  if (totalStandardTime > 0) {
    progressPercentage = Math.min((totalActualTime / totalStandardTime) * 100, 100); // Cap at 100%
  }

  const progressElement = document.getElementById(`truck-${truck.id}-progress`);
  progressElement.textContent = `${progressPercentage.toFixed(0)}%`; // Display with 0 decimal places 
}
```javascript
$(document).ready(function() {
    $('.edit-note-trigger').click(function() { 
       $(this).siblings('.note-content').hide();
       $(this).siblings('.edit-note-form').show();
   });

   $('.save-note').click(function() {
       let form = $(this).closest('.edit-note-form');
       let noteId = form.data('note-id');
       let newContent = form.find('textarea').val(); 

       // AJAX Call (update note using noteId and newContent) 
       $.ajax({
           // You'll need to populate url, method('POST'), dataType
           data: {note_id: noteId, content: newContent},
           success: function(data) {
               // update .note-content with data.updated_content
               // Handle errors with data.error etc.
           }
       });
    });
}); 