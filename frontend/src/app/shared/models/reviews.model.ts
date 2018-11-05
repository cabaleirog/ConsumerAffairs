export interface Reviewer {
    from: string;
    image_url: string;
    is_verified_buyer: boolean;
    is_verified_reviewer: boolean;
    name: string;
}

export interface Review {
    reviewer: Reviewer;
    company_response_date: string;
    company_response_text: string;
    customer_response_date: string;
    customer_response_text: string;
    helpful: number;
    id: number;
    original_review_date: string;
    stars: number;
    original_stars: number;
    resolution_in_progress: boolean;
    review: string;
    review_id: number;
    is_verified: boolean;  // Deprecated
    reviewer_image: string;  // Deprecated
    verified_buyer: boolean;  // Deprecated
    verified_reviewer: boolean;  // Deprecated
}

export interface CompanyInfo {
    company_logo_url: string;
    name: string;
}

export interface APIResponseReviews {
    company: CompanyInfo;
    reviews: Review[];
    page: number;
    total_reviews: number;
}
