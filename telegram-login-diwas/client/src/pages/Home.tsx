import { useEffect, useState } from "react";
import { useAuth } from "@/_core/hooks/useAuth";
import { Button } from "@/components/ui/button";
import { getLoginUrl } from "@/const";

export default function Home() {
  const { user, loading, isAuthenticated, logout } = useAuth();
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [userInfo, setUserInfo] = useState<any>(null);
  const [showAnimation, setShowAnimation] = useState(false);

  useEffect(() => {
    // Check if user is already logged in via Manus OAuth
    if (isAuthenticated && user) {
      setIsLoggedIn(true);
      setUserInfo(user);
      setShowAnimation(true);
    }

    // Check for Telegram login data in localStorage
    const telegramUser = localStorage.getItem("telegramUser");
    if (telegramUser) {
      try {
        const parsedUser = JSON.parse(telegramUser);
        setIsLoggedIn(true);
        setUserInfo(parsedUser);
        setShowAnimation(true);
      } catch (e) {
        console.error("Failed to parse Telegram user data:", e);
      }
    }
  }, [isAuthenticated, user]);

  // Telegram widget callback
  useEffect(() => {
    const handleTelegramAuth = (telegramUser: any) => {
      console.log("Telegram user:", telegramUser);
      localStorage.setItem("telegramUser", JSON.stringify(telegramUser));
      setIsLoggedIn(true);
      setUserInfo(telegramUser);
      setShowAnimation(true);
    };

    // Expose the callback globally for the Telegram widget
    (window as any).onTelegramAuth = handleTelegramAuth;

    // Load Telegram widget script
    const script = document.createElement("script");
    script.src = "https://telegram.org/js/telegram-widget.js?22";
    script.async = true;
    document.body.appendChild(script);

    return () => {
      if (document.body.contains(script)) {
        document.body.removeChild(script);
      }
    };
  }, []);

  const handleLogout = () => {
    setIsLoggedIn(false);
    setUserInfo(null);
    setShowAnimation(false);
    localStorage.removeItem("telegramUser");
    logout();
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-black">
        <div className="text-cyan text-glow text-2xl animate-pulse">
          [ SYSTEM INITIALIZING... ]
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-black text-white overflow-hidden">
      {/* Background grid effect */}
      <div className="fixed inset-0 bg-scanline pointer-events-none z-0"></div>

      {/* Main content */}
      <div className="relative z-10 flex flex-col items-center justify-center min-h-screen px-4">
        {!isLoggedIn ? (
          // Login screen
          <div className="w-full max-w-2xl">
            {/* Error code display */}
            <div className="text-center mb-12">
              <div className="error-code mb-6 text-red-500">
                [ ERROR_SYSTEM_FAILURE_001 ]
              </div>
              <div className="bracket-left bracket-right text-cyan text-lg mb-8">
                AUTHENTICATION PROTOCOL REQUIRED
              </div>
            </div>

            {/* 3D Diwas text animation */}
            <div className="flex justify-center mb-16">
              <div className="diwas-3d text-white text-center">DIWAS</div>
            </div>

            {/* Description */}
            <div className="text-center mb-12 space-y-4">
              <p className="text-cyan text-glow text-sm md:text-base">
                [ SYSTEM STATUS: AWAITING AUTHENTICATION ]
              </p>
              <p className="text-gray-400 text-xs md:text-sm font-mono">
                Establish secure connection via Telegram Login Protocol
              </p>
            </div>

            {/* Telegram login widget container */}
            <div className="flex flex-col items-center gap-8">
              <div className="terminal-border p-8 w-full max-w-sm">
                <div className="flex justify-center">
                  <div
                    data-telegram-login="Gate_ScannerBot"
                    data-size="large"
                    data-onauth="onTelegramAuth(user)"
                    data-request-access="write"
                  ></div>
                </div>
              </div>

              {/* Alternative login option */}
              {!isAuthenticated && (
                <div className="text-center">
                  <p className="text-gray-500 text-xs mb-4">
                    OR USE MANUS OAUTH
                  </p>
                  <Button
                    onClick={() => {
                      window.location.href = getLoginUrl();
                    }}
                    className="bg-cyan text-black hover:bg-cyan/80 font-bold px-8 py-2"
                  >
                    Login with Manus
                  </Button>
                </div>
              )}
            </div>

            {/* System status footer */}
            <div className="mt-16 text-center">
              <div className="text-gray-600 text-xs font-mono space-y-1">
                <p>[ SECURITY_LEVEL: HIGH ]</p>
                <p>[ ENCRYPTION: AES-256 ]</p>
                <p>[ STATUS: READY ]</p>
              </div>
            </div>
          </div>
        ) : (
          // Dashboard screen after login
          <div
            className={`w-full max-w-4xl transition-all duration-1000 ${
              showAnimation
                ? "opacity-100 scale-100"
                : "opacity-0 scale-95"
            }`}
          >
            {/* Success animation */}
            <div className="text-center mb-12">
              <div className="text-lime text-glow text-2xl mb-4 animate-pulse">
                [ AUTHENTICATION SUCCESSFUL ]
              </div>
              <div className="glitch text-cyan text-4xl md:text-5xl font-bold mb-8">
                WELCOME
              </div>
            </div>

            {/* User info display */}
            <div className="terminal-border p-8 mb-8 bg-black/50">
              <div className="space-y-4 font-mono text-sm">
                {userInfo?.first_name && (
                  <div className="flex justify-between">
                    <span className="text-cyan">[ USER_NAME ]</span>
                    <span className="text-white">
                      {userInfo.first_name}{" "}
                      {userInfo.last_name || ""}
                    </span>
                  </div>
                )}
                {userInfo?.id && (
                  <div className="flex justify-between">
                    <span className="text-cyan">[ USER_ID ]</span>
                    <span className="text-white">{userInfo.id}</span>
                  </div>
                )}
                {userInfo?.username && (
                  <div className="flex justify-between">
                    <span className="text-cyan">[ USERNAME ]</span>
                    <span className="text-white">@{userInfo.username}</span>
                  </div>
                )}
                {userInfo?.email && (
                  <div className="flex justify-between">
                    <span className="text-cyan">[ EMAIL ]</span>
                    <span className="text-white">{userInfo.email}</span>
                  </div>
                )}
                {userInfo?.name && (
                  <div className="flex justify-between">
                    <span className="text-cyan">[ ACCOUNT_NAME ]</span>
                    <span className="text-white">{userInfo.name}</span>
                  </div>
                )}
              </div>
            </div>

            {/* System status */}
            <div className="text-center mb-8 space-y-2">
              <p className="text-lime text-glow text-sm">
                [ SYSTEM_STATUS: OPERATIONAL ]
              </p>
              <p className="text-gray-400 text-xs">
                [ TIMESTAMP: {new Date().toLocaleString()} ]
              </p>
            </div>

            {/* Action buttons */}
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Button
                onClick={handleLogout}
                className="bg-red-600 hover:bg-red-700 text-white font-bold px-8 py-2"
              >
                [ LOGOUT ]
              </Button>
              <Button
                onClick={() => {
                  // Placeholder for additional actions
                  alert("Additional features coming soon...");
                }}
                className="bg-magenta hover:bg-magenta/80 text-black font-bold px-8 py-2"
              >
                [ SYSTEM_MENU ]
              </Button>
            </div>

            {/* Footer info */}
            <div className="mt-12 text-center">
              <div className="text-gray-600 text-xs font-mono space-y-1">
                <p>[ SECURITY_LEVEL: VERIFIED ]</p>
                <p>[ SESSION_ACTIVE: TRUE ]</p>
                <p>[ THREAT_LEVEL: NONE ]</p>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
