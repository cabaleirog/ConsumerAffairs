import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { CategoriesComponent } from './categories/categories.component';
import { CompaniesComponent } from './companies/companies.component';
import { NavbarComponent } from './layout/navbar/navbar.component';
import { ReviewsComponent } from './reviews/reviews.component';
import { SpinnerComponent } from './spinner/spinner.component';
import { RatingComponent } from './rating/rating.component';
import { HelpfulComponent } from './reviews/helpful/helpful.component';
import { UserImageComponent } from './user-image/user-image.component';
import { RouterModule, Routes } from '@angular/router';
import { ReviewsService } from './services/reviews.service';
import { HttpClientModule } from '@angular/common/http';

const appRoutes: Routes = [
    { path: 'categories', component: CategoriesComponent },
    { path: 'reviews', component: ReviewsComponent },
    { path: 'companies', component: CompaniesComponent },
    { path: '**', component: ReviewsComponent }
];

@NgModule({
    declarations: [
        AppComponent,
        CategoriesComponent,
        CompaniesComponent,
        NavbarComponent,
        ReviewsComponent,
        SpinnerComponent,
        RatingComponent,
        HelpfulComponent,
        UserImageComponent
    ],
    imports: [
        BrowserModule,
        AppRoutingModule,
        HttpClientModule,
        RouterModule.forRoot(
            appRoutes,
            { enableTracing: true }
        )
    ],
    providers: [ReviewsService],
    bootstrap: [AppComponent]
})
export class AppModule { }
