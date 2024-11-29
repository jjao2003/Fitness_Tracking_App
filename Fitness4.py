import flet as ft

def main(page: ft.Page):
    page.title = "Fitness App"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.theme_mode = "light"

    # Set a unique background color
    page.bgcolor = ft.colors.LIGHT_BLUE_100

    # Predefined exercises
    predefined_exercises = [
        {"name": "Push-Ups", "target": 20, "unit": "reps"},
        {"name": "Sit-Ups", "target": 50, "unit": "reps"},
        {"name": "Deadlift", "target": 20, "unit": "sets"},
        {"name": "Overhead Press", "target": 20, "unit": "sets"},
        {"name": "Bench Press", "target": 20, "unit": "sets"},
        {"name": "Walking", "target": 100000, "unit": "steps"},
        {"name": "Squats", "target": 30, "unit": "reps"},
        {"name": "Lunges", "target": 30, "unit": "reps"},
    ]

    # Fitness activities data with SI units
    activities = []

    # Function to update the activity list display
    def update_activity_list():
        activity_list.controls.clear()
        for index, activity in enumerate(activities):
            is_completed = activity["progress"] >= activity["target"]
            progress_bar = ft.ProgressBar(
                value=activity["progress"] / activity["target"],
                width=400,
                height=20,
                color="green" if is_completed else "blue",
            )
            check_mark = ft.Icon(
                name=ft.icons.CHECK_CIRCLE,
                color="green",
                size=24,
                visible=is_completed,
            )

            # Each activity row with options to update or delete
            activity_list.controls.append(
                ft.Container(
                    content=ft.Row(
                        controls=[
                            ft.Column(
                                controls=[
                                    ft.Text(
                                        f"{activity['name']}: {activity['progress']}/{activity['target']} {activity['unit']}",
                                        size=16,
                                        weight="bold",
                                    ),
                                    progress_bar,
                                ],
                                alignment=ft.MainAxisAlignment.CENTER,
                                spacing=10,
                            ),
                            ft.Column(
                                controls=[
                                    ft.Row(
                                        controls=[
                                            check_mark,
                                            ft.IconButton(
                                                icon=ft.icons.EDIT,
                                                tooltip="Update",
                                                on_click=lambda e, idx=index: open_update_activity_dialog(idx),
                                            ),
                                            ft.IconButton(
                                                icon=ft.icons.DELETE,
                                                tooltip="Delete",
                                                on_click=lambda e, idx=index: delete_activity(idx),
                                            ),
                                        ],
                                        spacing=10,
                                    ),
                                ],
                                alignment=ft.MainAxisAlignment.CENTER,
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        spacing=30,
                    ),
                    padding=ft.padding.all(10),
                    bgcolor=ft.colors.WHITE,
                    border_radius=10,
                    shadow=ft.BoxShadow(
                        blur_radius=5,
                        spread_radius=2,
                        color=ft.colors.GREY_400,
                    ),
                )
            )
        page.update()

    # Function to add a new activity
    def add_activity(e):
        try:
            selected_exercise = exercise_selector.value
            progress = int(activity_progress.value)

            if selected_exercise and progress >= 0:
                # Find the selected exercise details
                exercise = next((ex for ex in predefined_exercises if ex["name"] == selected_exercise), None)
                if exercise:
                    activities.append({
                        "name": exercise["name"],
                        "target": exercise["target"],
                        "progress": progress,
                        "unit": exercise["unit"]
                    })
                    activity_progress.value = ""
                    update_activity_list()
                else:
                    page.snack_bar = ft.SnackBar(ft.Text("Invalid exercise selected!"))
                    page.snack_bar.open = True
            else:
                page.snack_bar = ft.SnackBar(ft.Text("Please provide valid inputs!"))
                page.snack_bar.open = True
        except ValueError:
            page.snack_bar = ft.SnackBar(ft.Text("Progress must be a valid number!"))
            page.snack_bar.open = True
        page.update()

    # Function to delete an activity
    def delete_activity(index):
        del activities[index]
        update_activity_list()

    # Function to open the update dialog
    def open_update_activity_dialog(index):
        activity_to_update = activities[index]
        update_name.value = activity_to_update["name"]
        update_target.value = str(activity_to_update["target"])
        update_progress.value = str(activity_to_update["progress"])

        def save_update(e):
            try:
                activities[index]["name"] = update_name.value
                activities[index]["target"] = int(update_target.value)
                activities[index]["progress"] = int(update_progress.value)
                # Keep the unit unchanged
                update_activity_list()
                update_dialog.open = False
                page.update()
            except ValueError:
                page.snack_bar = ft.SnackBar(ft.Text("Please provide valid inputs!"))
                page.snack_bar.open = True

        update_dialog.actions = [ft.ElevatedButton("Save", on_click=save_update)]
        update_dialog.open = True
        page.update()

    # Dialog for updating an activity
    update_name = ft.TextField(label="Activity Name", width=250)
    update_target = ft.TextField(label="Target", width=100)
    update_progress = ft.TextField(label="Progress", width=100)
    update_dialog = ft.AlertDialog(
        title=ft.Text("Update Activity"),
        content=ft.Column([update_name, update_target, update_progress]),
    )

    # Weekly summary display
    summary_container = ft.Container(
        content=ft.Text("No activities yet.", size=16),
        padding=ft.padding.all(10),
        bgcolor=ft.colors.WHITE,
        border_radius=10,
        shadow=ft.BoxShadow(
            blur_radius=5,
            spread_radius=2,
            color=ft.colors.GREY_400,
        ),
        width=400,
    )

    def show_summary(e):
        if not activities:
            summary_container.content = ft.Text("No activities yet.", size=16)
        else:
            summary = "Weekly Summary:\n\n"
            for activity in activities:
                summary += f"{activity['name']}: {activity['progress']}/{activity['target']} {activity['unit']}\n"
            summary_container.content = ft.Text(summary, size=16)
        page.update()

    # Dropdown for selecting predefined exercises
    exercise_selector = ft.Dropdown(
        label="Select Exercise",
        options=[ft.dropdown.Option(ex["name"]) for ex in predefined_exercises],
        width=250
    )
    
    # Input field for progress
    activity_progress = ft.TextField(label="Progress", width=100)
    add_button = ft.ElevatedButton("Add Activity", on_click=add_activity)

    # Activity list display container
    activity_list = ft.Column(spacing=20)

    # Layout
    page.add(
        ft.Column(
            controls=[
                ft.Text("Fitness App", size=30, weight="bold"),
                ft.Row(
                    controls=[exercise_selector, activity_progress, add_button],
                    spacing=10,
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                ft.Text("Activities:", size=20, weight="bold"),
                activity_list,
                ft.ElevatedButton("Show Weekly Summary", on_click=show_summary),
                summary_container,  # Updated summary display
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=20,
        )
    )
    page.dialog = update_dialog
    update_activity_list()
    page.update()

ft.app(target=main)