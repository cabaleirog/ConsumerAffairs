import { Component, OnInit } from '@angular/core';
import { CategoriesService } from '../services/categories.service';
import { Category } from '../shared/models';

@Component({
    selector: 'app-categories',
    templateUrl: './categories.component.html',
    styleUrls: ['./categories.component.scss']
})
export class CategoriesComponent implements OnInit {
    categories: Category[];

    constructor(private categoriesService: CategoriesService) { }

    ngOnInit() {
        this.categoriesService.fetchCategories().subscribe(response => {
            console.log(response);
            this.categories = response['data'];
        });
    }

}
