import { useEffect, useCallback } from 'react';
import { useNavigate } from 'react-router-dom';

export const useScreenshotDetection = () => {
  const navigate = useNavigate();

  const handleScreenshotDetected = useCallback(() => {
    console.warn('Screenshot or screen recording detected!');
    navigate('/payment');
  }, [navigate]);

  useEffect(() => {
    const handleKeyDown = (event: KeyboardEvent) => {
      const isScreenshotShortcut =
        event.key === 'PrintScreen' ||
        (event.altKey && event.key === 'PrintScreen') ||
        (event.metaKey && event.key === 'PrintScreen') ||
        (event.metaKey && event.shiftKey && ['3', '4', '5'].includes(event.key)) ||
        (event.metaKey && event.shiftKey && event.key.toLowerCase() === 's'); // Win+Shift+S

      if (isScreenshotShortcut) {
        event.preventDefault();
        handleScreenshotDetected();
      }
    };

    const handleDevToolsShortcut = (event: KeyboardEvent) => {
      if (
        event.key === 'F12' ||
        (event.ctrlKey && event.shiftKey && event.key === 'I') ||
        (event.metaKey && event.altKey && event.key === 'I') ||
        (event.ctrlKey && event.key === 'U')
      ) {
        event.preventDefault();
        handleScreenshotDetected();
      }
    };

    const handleContextMenu = (event: MouseEvent) => {
      event.preventDefault();
      handleScreenshotDetected();
    };

    const handleVisibilityChange = () => {
      if (document.hidden) {
        setTimeout(() => {
          if (document.hidden) {
            handleScreenshotDetected();
          }
        }, 800);
      }
    };

    const handleBlur = () => {
      // On mobile, screenshot often causes blur event
      setTimeout(() => {
        if (document.hidden) {
          handleScreenshotDetected();
        }
      }, 1000);
    };

    document.addEventListener('keydown', handleKeyDown);
    document.addEventListener('keydown', handleDevToolsShortcut);
    document.addEventListener('visibilitychange', handleVisibilityChange);
    document.addEventListener('contextmenu', handleContextMenu);
    window.addEventListener('blur', handleBlur);

    return () => {
      document.removeEventListener('keydown', handleKeyDown);
      document.removeEventListener('keydown', handleDevToolsShortcut);
      document.removeEventListener('visibilitychange', handleVisibilityChange);
      document.removeEventListener('contextmenu', handleContextMenu);
      window.removeEventListener('blur', handleBlur);
    };
  }, [handleScreenshotDetected]);

  return { handleScreenshotDetected };
};
