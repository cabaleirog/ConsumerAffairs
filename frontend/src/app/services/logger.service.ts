import { Injectable } from '@angular/core';
import { environment } from '../../environments/environment';

interface Logger {
    debug(msg): void;
    warn(msg): void;
    error(msg): void;
}


@Injectable({
    providedIn: 'root'
})
export class ConsoleLoggerService implements Logger {

    constructor() { }

    debug(msg): void {
        // avoid logging debug messages on production.
        if (!environment.production) {
            console.log(msg);
        }
    }

    warn(msg): void {
        console.warn(msg);
    }

    error(msg): void {
        console.error(msg);
    }
}
