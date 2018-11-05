import { Component, OnInit, Input } from '@angular/core';

@Component({
    selector: 'app-user-image',
    templateUrl: './user-image.component.html',
    styleUrls: ['./user-image.component.scss']
})
export class UserImageComponent implements OnInit {
    @Input() imageUrl: string;

    constructor() { }

    ngOnInit() { }

}
