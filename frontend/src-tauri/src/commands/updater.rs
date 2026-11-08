//! GoreeCloud PDF Manager desktop update policy.
//!
//! The upstream Tauri updater was intentionally removed from this development
//! preview. No update endpoint, signing key, download, or installation is trusted
//! until a GoreeCloud-controlled release and signing process is verified.
//!
//! Preserve command contracts so old UI paths receive safe, explicit responses.
use serde::{Deserialize, Serialize};
use tauri::AppHandle;

#[derive(Serialize, Deserialize, Clone, Debug)]
#[serde(rename_all = "camelCase")]
pub struct UpdateInfo {
    pub version: String,
    pub current_version: String,
    pub release_notes: Option<String>,
}

#[derive(Serialize, Clone, Debug)]
#[serde(rename_all = "camelCase")]
pub struct CanInstallResult {
    pub can_install: bool,
    pub reason: Option<String>,
    pub install_dir: Option<String>,
}

/// Deliberately avoid all outbound version checks or release metadata requests.
#[tauri::command]
pub async fn check_for_update(_app: AppHandle) -> Result<Option<UpdateInfo>, String> {
    Ok(None)
}

/// Fail closed; this preview has no trusted installer or updater signing key.
#[tauri::command]
pub async fn download_and_install_update(_app: AppHandle) -> Result<(), String> {
    Err("Automatic updates are unavailable in GoreeCloud PDF Manager development preview".into())
}

#[tauri::command]
pub fn restart_app(app: AppHandle) {
    app.restart();
}

#[tauri::command]
pub fn get_app_version(app: AppHandle) -> String {
    app.package_info().version.to_string()
}

/// Never report update installation permission when installation is disabled.
#[tauri::command]
pub fn can_install_updates() -> CanInstallResult {
    CanInstallResult {
        can_install: false,
        reason: Some("updater_disabled".to_string()),
        install_dir: None,
    }
}

#[cfg(test)]
mod tests {
    use super::can_install_updates;
    #[test]
    fn disabled_updater_cannot_install() {
        let status = can_install_updates();
        assert!(!status.can_install);
        assert_eq!(status.reason.as_deref(), Some("updater_disabled"));
        assert!(status.install_dir.is_none());
    }
}
