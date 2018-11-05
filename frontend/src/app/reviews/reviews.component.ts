import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { ReviewsService } from '../services/reviews.service';

export interface PageData {
    page: number;
    requesting: boolean;
    loaded: boolean;
    count: number;
    data: any;
}

export interface PageGroup {
    page: number;
    data: PageData;
}

@Component({
    selector: 'app-reviews',
    templateUrl: './reviews.component.html',
    styleUrls: ['./reviews.component.scss']
})
export class ReviewsComponent implements OnInit {
    // reviews$: Observable<any[]>;
    reviews: any;
    company: any;
    currentPage: number;
    isLoading = true;
    lastPage: number = null;
    breadcrumbs: string[];
    subscription: any;
    private companyUrl: string;
    private pages: PageData[] = [];
    private auxPageNumber: number;

    private keepFetchedData = true;
    private loadAllDataInBackground = false;

    constructor(private reviewsService: ReviewsService, private route: ActivatedRoute) {
        this.currentPage = 1;
        this.auxPageNumber = this.currentPage;
    }

    ngOnInit() {
        this.route.paramMap.subscribe(params => {
                console.log('paramMap results');
                console.log(params);

                this.companyUrl = params.get('url');

                // List to be used to query Firebase
                this.breadcrumbs = [
                    params.get('category'),
                    params.get('subcategory'),
                    params.get('company')
                ];

                console.log(this.breadcrumbs);

            });
        this.fetchReviews();
    }

    goToNextPage = () => {
        this.currentPage++;
        this.fetchOrAssign(this.currentPage);
    }

    goToPreviousPage = () => {
        this.currentPage--;
        this.fetchOrAssign(this.currentPage);
    }

    isPageAvailable = (pageNumber) => {
        if (this.loadAllDataInBackground) {
            const page = this.pageData(pageNumber);
            return (page !== undefined && (page.requesting || page.loaded));
        } else {
            // ToDo: Handle exception for last page.
            return true;
        }
    }

    private fetchOrAssign = (pageNumber: number) => {
        console.log('FetchOrAssign', pageNumber, this.pages);
        const data = this.pageData(pageNumber);
        if (data === undefined) {
            this.fetchReviews(pageNumber);
        } else if (!data.loaded && !data.requesting) {
            this.fetchReviews(pageNumber);
        } else {
            this.reviews = this.pageData(this.currentPage).data;
        }
    }

    private pageData = (pageNumber) => this.pages.find(x => x.page === pageNumber);

    private fetchReviews = (pageNumber?: number) => {
        const pageToRetrive = pageNumber ? pageNumber : this.currentPage;
        console.log('FetchReviews', pageToRetrive, this.pageData(pageToRetrive));
        if (this.pageData(pageToRetrive) === undefined) {
            this.pages.push({ page: pageToRetrive, requesting: true, loaded: false, count: 0, data: undefined });
        }
        if (pageToRetrive === this.currentPage) {
            this.isLoading = true;
        }

        this.reviewsService.fetchReviews(this.companyUrl)
            .subscribe((data) => {
                this.reviews = data.reviews;
                this.company = data.company;
                console.log(this.reviews);
            });

        // this.subscription = this.dataService.getTestingReviews()
        //   // this.subscription = this.dataService.getReviews(this.companyUrl, this.currentPage)
        //   //   .map(response => response = response['results'])
        //   // this.subscription = this.dataService.getFirebaseReviews(this.breadcrumbs, 3)
        //   .subscribe(response => {
        //     console.log(response);
        //     this.reviews = response;
        //   });

    }

}
