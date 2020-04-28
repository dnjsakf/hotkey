import pyautogui
import win32api
import win32gui
import win32ui
import win32con
import win32clipboard

from pynput.keyboard import Listener, Key, KeyCode


def screenshot(hwin=None):
  print('screenshot')
  
  if hwin and hwin > 0:
    # 좌표 및 사이즈 가져오기
    left, top, width, height = win32gui.GetClientRect( hwin )
    
    hwindc = win32gui.GetWindowDC(hwin)
    srcdc = win32ui.CreateDCFromHandle(hwindc)
    memdc = srcdc.CreateCompatibleDC()
    
    # bmp(비트맵)으로 저장
    bmp = win32ui.CreateBitmap()    
    bmp.CreateCompatibleBitmap(srcdc, width, height)
    
    memdc.SelectObject(bmp)
    memdc.BitBlt((0, 0), (width, height), srcdc, (left, top), win32con.SRCCOPY)
    
    bmp.SaveBitmapFile(memdc, "test.bmp")
    win32gui.DeleteObject(bmp.GetHandle())
    
    # png로 저장
    left, top = win32gui.ClientToScreen(hwin, (left, top))
    width, height = win32gui.ClientToScreen(hwin, (width - left, height - top))
    jpg = pyautogui.screenshot("test.png", region=(left, top, width, height))
    jpg.show() # 저장 후 열기
    
    # Clear
    memdc.DeleteDC()
    srcdc.DeleteDC()
    win32gui.ReleaseDC(hwin, hwindc)
    
  else:
    print('Not Found Window..')
    
def write_text(text=""):
  hwin = win32gui.GetDesktopWindow()
  hdc = win32gui.GetDC(hwin)
  
  # 텍스트 옵션
  font = win32ui.CreateFont({
    "name": "Arial",
    "height": 64,
    "weight": 400
  })
  oldFont = win32gui.SelectObject(hdc, font.GetSafeHandle())
  
  #win32gui.SetTextColor(hdc, win32api.RGB(0,0,0))
  #win32gui.SetBkColor(hdc, win32api.RGB(255, 255, 255))
  
  rect = win32gui.GetClientRect(hwin)
  win32gui.DrawText(hdc, text, len(text), rect, 
    win32con.DT_BOTTOM|win32con.DT_RIGHT|win32con.DT_SINGLELINE|win32con.DT_WORDBREAK
    #win32con.DT_CENTER|win32con.DT_VCENTER|win32con.DT_SINGLELINE|win32con.DT_WORDBREAK
  )
  
  win32gui.SelectObject(hdc, oldFont)
  win32gui.DeleteObject(font.GetSafeHandle())
  win32gui.ReleaseDC(hwin, hdc)
    
def draw_pixel():
  hwin = win32gui.GetDesktopWindow()
  hdc = win32gui.GetDC(hwin)

  # 점찍기
  red = win32api.RGB(255, 0, 0)
  win32gui.SetPixel(hdc, 0, 0, red)
  win32gui.SetPixel(hdc, 0, 1, red)
  win32gui.SetPixel(hdc, 0, 2, red)
  win32gui.SetPixel(hdc, 0, 3, red)

  # 사각형그리기
  pen = win32gui.CreatePen(win32con.PS_SOLID, 5, win32api.RGB(0,0,255))
  oldPen = win32gui.SelectObject(hdc, pen)
  
  win32gui.Rectangle(hdc, 50, 50, 100, 100)
  win32gui.SelectObject(hdc, oldPen)
  win32gui.DeleteObject(pen)
  

def screenshot_desktop():
  # Desktop 전체 가져오기
  desktop = win32gui.GetDesktopWindow()
  
  screenshot(hwin=desktop)

def screenshot_foreground():
  # 현재 활성호된 Window 가져오기
  forground = win32gui.GetForegroundWindow()
  
  screenshot(hwin=forground)


store = set()
 
HOT_KEYS = {
  'screenshot_desktop': set([ Key.alt_l, KeyCode(char='1')] )
  , 'screenshot_foreground': set([ Key.alt_l, KeyCode(char='2')] )
  , 'draw_pixel': set([ Key.alt_l, KeyCode(char='3')] )
}

def handleKeyPress( key, **kwargs ):
  write_text( str(store) )
  store.add( key )
 
def handleKeyRelease( key ):
  for action, trigger in HOT_KEYS.items():
    CHECK = all([ True if triggerKey in store else False for triggerKey in trigger ])

    if CHECK:
      try:
        action = eval( action )
        if callable( action ):
          action()
      except NameError as err:
        print( err )
              
  # 종료
  if key == Key.esc:
    return False
  elif key in store:
    store.remove( key )
  
with Listener(on_press=handleKeyPress, on_release=handleKeyRelease) as listener:
  listener.join()
