function renderTimeDifference(timestamp) {
    const now = new Date();
    const notificationTime = new Date(timestamp);
    const timeDiff = Math.abs(now - notificationTime) / 1000; // in seconds
    const minutes = Math.floor(timeDiff / 60);
    const hours = Math.floor(timeDiff / 3600);
    const days = Math.floor(timeDiff / 86400);
    if (days > 0) {
        return notificationTime.toLocaleDateString(); // return date if older than a day
    } else if (hours > 0) {
        return hours + ' hours ago';
    } else if (minutes > 0) {
        return minutes + ' minutes ago';
    } else {
        return 'just now';
    }
}

function generateNotificationDetailUrl(idValue) {
    const id_placer_value = "ID_PLACER";
    const newUrl = CUrls["admin:notification_system_notification_change"];
    return newUrl.replace(id_placer_value, idValue);
}

function fetchRequest(args) {
    if (!args.beforeSend) {
        args.beforeSend = function (jqXHR) {
            jqXHR.setRequestHeader('X-CSRFToken', $('input[name=csrfmiddlewaretoken]').val());
        };
    }
    return $.ajax(args);
}

function fetchNotificationListMy() {
    const url = `${CUrls["admin_dashboard:user-notification-list-my-api"]}?unread=1`;
    fetchRequest({
        url: url,
        success: function (response) {
            let html = "";
            if (response.results.length > 0) {
                $.each(response.results, function (index, notificationItem) {
                    const time_data = renderTimeDifference(notificationItem.created_at);
                    html += `<a class="dropdown-item" href="${generateNotificationDetailUrl(notificationItem.id)}">${notificationItem.verb}<span class="float-right text-muted text-sm">${time_data}</span></a>`;
                });
            } else {
                html = '<a class="dropdown-item" href="#"> No new notifications </a>';
            }
            $('#dropdown-notifications-list .notifications-list').html(html);
            $('#dropdown-notifications-list .notifications-count').text(response.count);
            if (response.count > 0) {
                $('#dropdown-notifications-list .notifications-count-toggle').css('display', 'block');
            } else {
                $('#dropdown-notifications-list .notifications-count-toggle').css('display', 'none');
            }
        }
    });
}

Dropzone.autoDiscover = false;
$(document).ready(function () {
    fetchNotificationListMy();
    // $(window).on('hashchange', function () {
    //     console.log("link chnage");
    //     $(".preloader").css("height", "100vh");
    //     $(".preloader>div").css("display", "block");
    // });
    $(".image-with-thumbs-widget-container").each(function () {
        const el = $(this);
        const raw_data = el.data();
        const raw_data_value = raw_data.value;
        const data = {
            'app_name': raw_data.app_name,
            'model_name': raw_data.model_name,
            'object_id': raw_data.object_id,
            'field_name': raw_data.field_name,
            'field_type': raw_data.field_type,
            'field_method': raw_data.field_method,
            'value': raw_data_value ? {
                "name": raw_data_value.name,
                "relative_path": raw_data_value.relative_path,
                "url": raw_data_value.url,
            } : null,
        };
        const dropzone_id = `#dropzone-${data.field_name}`;
        const dropzoneEl = document.querySelector(dropzone_id);
        const previewNode = dropzoneEl.querySelector(".dropzone-item-template");
        previewNode.id = "";
        const previewTemplateHTML = previewNode.parentNode.innerHTML;
        previewNode.parentNode.removeChild(previewNode);

        const myDropzone = new Dropzone(dropzone_id, { // Make the whole body a dropzone
            url: CUrls['admin_dashboard:file-upload-api'], // Set the url for your upload script location
            parallelUploads: 20,
            maxFiles: 5,
            previewTemplate: previewTemplateHTML,
            maxFilesize: 2, // Max filesize in MB
            autoQueue: false, // Make sure the files aren't queued until manually added
            previewsContainer: dropzone_id + " .dropzone-items", // Define the container to display the previews
            clickable: dropzone_id + " .dropzone-select", // Define the element that should be used as click trigger to select files.
            headers: {
                'X-CSRFToken': $('input[name=csrfmiddlewaretoken]').val(),
            }
        });

        const imageSizeSelectEl = $(dropzone_id + ' .image-size-select');
        imageSizeSelectEl.select2();
        const dropzoneItemCurrentValueEl = $(dropzone_id + " .dropzone-item-current-value");

        myDropzone.on("addedfile", function (file) {
            // Hookup the start button
            file.previewElement.querySelector(dropzone_id + " .dropzone-start").onclick = function () {
                myDropzone.enqueueFile(file);
            };
            const dropzoneItems = dropzoneEl.querySelectorAll('.dropzone-item');
            dropzoneItems.forEach(dropzoneItem => {
                dropzoneItem.style.display = '';
            });
            dropzoneEl.querySelector('.dropzone-upload').style.display = "inline-block";
            dropzoneEl.querySelector('.dropzone-remove-all').style.display = "inline-block";
        });

        myDropzone.on("totaluploadprogress", function (progress) {
            const progressBars = dropzoneEl.querySelectorAll('.progress-bar');
            progressBars.forEach(progressBar => {
                progressBar.style.width = progress + "%";
            });
        });

        myDropzone.on("sending", function (file, xhr, formData) {
            const progressBars = dropzoneEl.querySelectorAll('.progress-bar');
            progressBars.forEach(progressBar => {
                progressBar.style.opacity = "1";
            });
            file.previewElement.querySelector(dropzone_id + " .dropzone-start").setAttribute("disabled", "disabled");


            formData.append('name', file.name);
            formData.append('app_name', data.app_name);
            formData.append('model_name', data.model_name);
            formData.append('model_field_name', data.field_name);
            formData.append('method', data.field_method);
            formData.append('type', data.field_type);
            formData.append('object_id', data.object_id);

            const sizes = imageSizeSelectEl.val().replace(")", "").replace("(", "").split(",").map(function (item) {
                return Number(item);
            })
            formData.append('sizes_width', sizes[0])
            formData.append('sizes_height', sizes[1])
        });

        myDropzone.on("complete", function () {
            const progressBars = dropzoneEl.querySelectorAll('.dz-complete');

            setTimeout(function () {
                progressBars.forEach(progressBar => {
                    progressBar.querySelector('.progress-bar').style.opacity = "0";
                    progressBar.querySelector('.progress').style.opacity = "0";
                    progressBar.querySelector('.dropzone-start').style.opacity = "0";
                });
            }, 300);
        });

        function setCurrentValue(response = null) {
            if (response === null) {
                dropzoneItemCurrentValueEl.css("display", "none");
            } else {
                dropzoneItemCurrentValueEl.find(".dropzone-filename").attr("title", response.name);
                dropzoneItemCurrentValueEl.find(".dropzone-filename a").html(response.name);
                dropzoneItemCurrentValueEl.find("[data-dz-size]").html(`${response.size}kb`);
                dropzoneItemCurrentValueEl.css("display", "block");
            }
        }

        myDropzone.on('success', function (file, response) {
            setCurrentValue(response);
        });

        myDropzone.on('error', function (file, errorMessage) {
            if (errorMessage.type === 'validation_error') {
                var errorDisplay = $(dropzone_id + ' [data-dz-errormessage]').first();
                var html = "";
                errorMessage.errors.forEach(function (item) {
                    html += `<li>[${item.attr}.${item.code}]${item.detail}</li>`;
                });
                errorDisplay.html(`<ul>${html}</ul>`);
            } else {
                alert("Unexpected error");
            }
        });

        dropzoneEl.querySelector(".dropzone-upload").addEventListener('click', function () {
            myDropzone.enqueueFiles(myDropzone.getFilesWithStatus(Dropzone.ADDED));
        });

        dropzoneEl.querySelector(".dropzone-remove-all").addEventListener('click', function () {
            dropzoneEl.querySelector('.dropzone-upload').style.display = "none";
            dropzoneEl.querySelector('.dropzone-remove-all').style.display = "none";
            myDropzone.removeAllFiles(true);
        });

        myDropzone.on("queuecomplete", function () {
            const uploadIcons = dropzoneEl.querySelectorAll('.dropzone-upload');
            uploadIcons.forEach(uploadIcon => {
                uploadIcon.style.display = "none";
            });
        });

        myDropzone.on("removedfile", function () {
            if (myDropzone.files.length < 1) {
                dropzoneEl.querySelector('.dropzone-upload').style.display = "none";
                dropzoneEl.querySelector('.dropzone-remove-all').style.display = "none";
            }
        });

        dropzoneItemCurrentValueEl.find(".dropzone-delete").click(function () {
            setCurrentValue();
        });
    });
});