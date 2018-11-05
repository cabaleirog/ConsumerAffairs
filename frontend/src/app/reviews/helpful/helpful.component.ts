import { Component, OnInit, Input } from '@angular/core';
import { ConsoleLoggerService } from 'src/app/services/logger.service';

@Component({
    selector: 'app-helpful',
    templateUrl: './helpful.component.html',
    styleUrls: ['./helpful.component.scss']
})
export class HelpfulComponent implements OnInit {
    private logger: ConsoleLoggerService;
    @Input() currentLikes: number;
    clicked = false;

    constructor(logger: ConsoleLoggerService) {
        this.logger = logger;
    }

    ngOnInit() {
        // Cleanup
        if (this.currentLikes === null) {
            this.currentLikes = 0;
        }
    }

    onClick(): void {
        this.logger.debug('Helpful clicked by the user');
        // ToDo: Handle the event using an API to store the action.
        this.currentLikes++;
        this.clicked = true;
    }

}
