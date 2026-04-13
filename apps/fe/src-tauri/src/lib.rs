// MTrans Desktop - Main Entry Point

#[cfg_attr(mobile, tauri::mobile_entry_point)]
pub fn run() {
    tauri::Builder::default()
        .plugin(tauri_plugin_shell::init())
        .invoke_handler(tauri::generate_handler![
            commands::list_audio_devices,
            commands::start_translation,
            commands::stop_translation,
            commands::get_status,
            commands::check_virtual_mic,
        ])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}

pub mod audio;
pub mod commands;
pub mod ws;
