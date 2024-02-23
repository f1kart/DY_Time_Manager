@app.route('/task/<int:task_id>/stop', methods=['POST'])
def stop_timer(task_id):
    # ... (Authentication Logic)
    time_entry = TimeEntry.query.filter_by(
        # ...
    ).order_by(TimeEntry.start_time.desc()).first()  # Find most recent entry

    if time_entry:
        time_entry.end_time = datetime.now()  # Set the stop time
        time_entry.duration = time_entry.end_time - time_entry.start_time
        task = time_entry.task
        if task.status == TaskStatus.IN_PROGRESS:  # Make sure this stop aligns with an active task
            task.status = TaskStatus.COMPLETE
        db.session.commit()
    # ... (Rest of Route)