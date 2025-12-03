import { useEffect } from 'react';

export default function Home() {
  useEffect(() => {
    // Load Telegram widget script
    const script = document.createElement('script');
    script.src = 'https://telegram.org/js/telegram-widget.js?22';
    script.async = true;
    document.body.appendChild(script);

    // Define the callback function globally
    (window as any).onTelegramAuth = function (user: any) {
      const message = `Logged in as ${user.first_name} ${user.last_name || ''} (${user.id}${user.username ? ', @' + user.username : ''})`;
      alert(message);
      console.log('User authenticated:', user);
    };

    return () => {
      // Cleanup if needed
    };
  }, []);

  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-gradient-to-br from-orange-900 via-red-900 to-yellow-900 relative overflow-hidden">
      {/* Animated background lights */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        <div className="absolute top-20 left-10 w-72 h-72 bg-orange-500 rounded-full mix-blend-multiply filter blur-3xl opacity-20 animate-blob"></div>
        <div className="absolute top-40 right-10 w-72 h-72 bg-yellow-500 rounded-full mix-blend-multiply filter blur-3xl opacity-20 animate-blob animation-delay-2000"></div>
        <div className="absolute -bottom-8 left-20 w-72 h-72 bg-red-500 rounded-full mix-blend-multiply filter blur-3xl opacity-20 animate-blob animation-delay-4000"></div>
      </div>

      <main className="relative z-10 flex flex-col items-center justify-center min-h-screen px-4">
        {/* 3D Diwas Text */}
        <div className="mb-12 text-center">
          <h1 className="diwas-3d-text text-7xl md:text-8xl font-bold mb-8">
            दिवास
          </h1>
          <p className="text-xl md:text-2xl text-yellow-100 font-light tracking-wide mb-2">
            Festival of Lights
          </p>
          <p className="text-lg text-orange-200 font-light">
            Welcome to the celebration
          </p>
        </div>

        {/* Telegram Login Widget */}
        <div className="bg-white bg-opacity-10 backdrop-blur-md rounded-2xl p-8 shadow-2xl border border-white border-opacity-20 flex flex-col items-center justify-center">
          <p className="text-white text-lg mb-6 font-light">
            Sign in with Telegram
          </p>
          
          {/* Telegram Widget Container */}
          <div
            className="telegram-widget-container"
            data-telegram-login="e_ScannerBot"
            data-size="large"
            data-onauth="onTelegramAuth(user)"
            data-request-access="write"
          ></div>
        </div>

        {/* Decorative elements */}
        <div className="mt-16 flex gap-4 justify-center flex-wrap">
          <div className="w-3 h-3 rounded-full bg-yellow-400 animate-pulse"></div>
          <div className="w-3 h-3 rounded-full bg-orange-400 animate-pulse animation-delay-1000"></div>
          <div className="w-3 h-3 rounded-full bg-red-400 animate-pulse animation-delay-2000"></div>
          <div className="w-3 h-3 rounded-full bg-yellow-400 animate-pulse animation-delay-3000"></div>
        </div>
      </main>
    </div>
  );
}
