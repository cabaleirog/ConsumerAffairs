import { Component, OnInit, Input } from '@angular/core';

@Component({
    selector: 'app-rating',
    templateUrl: './rating.component.html',
    styleUrls: ['./rating.component.scss']
})
export class RatingComponent implements OnInit {

    /**
     * The `rating` value.
     *
     * ```html
     * <app-rating rating=4></app-rating>
     * ```
     */
    @Input() rating: number;
    @Input() maxRating = 5;
    @Input() fillColor = '#FFCC66';
    @Input() strokeColor = '#FFCC66';

    private id: string;

    /**
     * ...............................
     */
    starRating: any[] = [];

    constructor() {
        this.id = (Math.floor(Math.random() * 10E12)).toString();
    }

    ngOnInit() {
        // if (this.rating === undefined) { this.rating = 0; }
        this.rating = this.rating || 0;

        for (let i = 0; i < this.maxRating; i++) {
            this.starRating.push({
                percentage: Math.max(0, Math.min(1, this.rating - i)),
                id: `grad_${this.id}_${i}`
            });

            // if (i === Math.floor(this.rating)) {
            //     this.starRating.push(this.rating - i);
            // } else if (i < this.rating) {
            //     this.starRating.push(1);
            // } else {
            //     this.starRating.push(0);
            // }
        }
        console.log(this.rating);
        console.log(this.starRating);
    }

}
