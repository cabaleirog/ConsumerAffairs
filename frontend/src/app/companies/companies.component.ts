import { Component, OnInit } from '@angular/core';
import { CompaniesService } from '../services/companies.service';
import { ActivatedRoute } from '@angular/router';

@Component({
    selector: 'app-companies',
    templateUrl: './companies.component.html',
    styleUrls: ['./companies.component.scss']
})
export class CompaniesComponent implements OnInit {
    companies: any[];
    private url: string;

    constructor(private companiesService: CompaniesService, private route: ActivatedRoute) { }

    ngOnInit() {
        this.route.paramMap.subscribe(params => {
            this.url = params.get('url');
            console.log(this.url);
        });
        this.companiesService.fetchCompanies(this.url).subscribe(response => {
            console.log(response);
            this.companies = response.data;
            console.log(this.companies);
        });
    }

}
