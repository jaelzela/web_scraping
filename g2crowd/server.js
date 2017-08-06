var fs = require('fs');
var request = require('request');
var cheerio = require('cheerio');
var srequest = require('sync-request');
async = require("async");

url_base = 'https://www.g2crowd.com';
url = 'https://www.g2crowd.com/categories/cloud-platform-as-a-service-paas';
apis = []
apis_keys = []
reviews = []

var services = [
    'business-services',
    'marketing-services-48f2fbc6-8574-4768-b810-e62f5c42b5d3',
    'it-outsourcing',
    'other-services',
    'technology-research',
    'implementation-services',
    'solution-consulting',
    'staffing-services',
    'translation-services',
    'value-added-resellers-vars'
]

software = [
    'crm-all-in-one',
    'contact-center-infrastructure',
    'contact-center-workforce',
    'telecom-services-for-call-centers',
    'customer-self-service',
    'customer-success',
    'employee-monitoring',
    'enterprise-feedback-management',
    'field-service-management',
    'help-desk',
    'live-chat',
    'other-customer-service',
    'proactive-notification',
    'social-customer-service',
    'account-based-execution',
    'account-based-reporting',
    'marketing-account-intelligence',
    'marketing-account-management',
    'attribution',
    'content-marketing',
    'conversion-rate-optimization',
    'brand-advocacy',
    'gamification-loyalty',
    'lead-generation',
    'digital-analytics',
    'digital-signage',
    'email-marketing',
    'audience-response',
    'event-management-platforms',
    'event-planning',
    'event-registration-ticketing',
    'mobile-event-apps',
    'other-event-management',
    'inbound-call-tracking',
    'marketing-analytics',
    'marketing-automation',
    'marketing-resource-management',
    'market-intelligence',
    'mobile-marketing',
    'multi-level-marketing-mlm',
    'online-reputation-management',
    'other-marketing',
    'print-fulfillment',
    'media-and-influencer-targeting',
    'media-monitoring',
    'other-public-relations',
    'pr-analytics',
    'press-release-distribution',
    'search-marketing',
    'influencer-marketing',
    'other-social-media',
    'social-analytics',
    'social-media-mgmt',
    'social-media-monitoring',
    'social-media-suites',
    'online-community-management',
    'contract-lifecycle-management-clm',
    'crm',
    'e-signature',
    'partner-management',
    'other-sales',
    'cpq',
    'pricing',
    'proposal',
    'email-tracking',
    'outbound-call-tracking',
    'sales-coaching-and-onboarding',
    'sales-enablement',
    'sales-performance-management',
    'sales-analytics',
    'sales-gamification',
    'sales-intelligence',
    'sfdc-appexchange-tools',
    'business-intelligence',
    'enterprise-search',
    'other-analytics',
    'predictive-analytics',
    'building-design-and-building-information-modeling-bim',
    'civil-engineering-design',
    'general-purpose-cad',
    'other-cad',
    'product-and-machine-design',
    'sketching',
    'computer-aided-engineering-cae',
    'gis',
    'plm',
    'idea-management',
    'note-taking-management',
    'other-collaboration',
    'social-networks',
    'structured-collaboration',
    'team-collaboration',
    'voip',
    'web-conferencing',
    'web-conferencing-personal',
    'business-content-management',
    'cms-tools',
    'content-analytics',
    'digital-asset-management',
    'enterprise-content-management-ecm',
    'file-storage-sharing',
    'localization',
    'web-content-management',
    'website-builder',
    'api-management',
    'api-marketplace',
    'alm-suites',
    'drag-and-drop-app-development',
    'mobile-analytics',
    'mobile-app-debugging',
    'mobile-app-optimization',
    'mobile-app-testing',
    'mobile-backend-as-a-service-mbaas',
    'mobile-cloud-communication-platforms',
    'mobile-development-frameworks',
    'mobile-development-platforms',
    'other-mobile-development',
    'low-code-development-platforms',
    'no-code-development-platforms',
    'bug-tracking',
    'cloud-platform-as-a-service-paas',
    'continuous-delivery',
    'text-editor',
    'wysiwyg-editors',
    'audio-engine',
    'game-engine',
    'gaming-tools',
    'physics-engine',
    'help-authoring-tool-hat',
    'integrated-development-environment-ide',
    'other-development',
    'portals',
    'peer-code-review',
    'static-code-analysis',
    'version-control-clients',
    'version-control-hosting',
    'version-control-systems',
    'test-management',
    'web-frameworks',
    'ad-network',
    'cross-channel-advertising',
    'demand-side-platform-dsp',
    'display-advertising',
    'mobile-advertising',
    'native-advertising',
    'search-advertising',
    'social-advertising',
    'video-advertising',
    'data-management-platform-dmp',
    'other-digital-advertising',
    'app-monetization',
    'other-publisher-management',
    'publisher-ad-server',
    'supply-side-platform-ssp',
    'e-commerce',
    'accounting',
    'billing',
    'corporate-performance-management-cpm',
    'corporate-tax',
    'governance-risk-compliance',
    'order-management',
    'other-finance-admin',
    'payroll',
    'pos',
    'procurement',
    'expense-management',
    'travel-management',
    'enterprise-asset-management-eam',
    'erp-suites',
    'professional-service-automation',
    'project-based-erp',
    'project-portfolio-management-ppm',
    'tools-for-erp',
    'content-delivery-network-cdn',
    'domain-registration',
    'managed-hosting',
    'other-hosting-services',
    'virtual-private-servers-vps',
    'website-hosting',
    'benefits-administration',
    'core-hr',
    'freelance-platforms',
    'hr-management-suites',
    'other-hr',
    'sales-compensation',
    'staffing',
    'compensation-management',
    'employee-engagement',
    'performance-management',
    'recruiting',
    'corporate-lms',
    'course-authoring',
    'time-tracking',
    'workforce-management',
    'application-performance-monitoring-apm',
    'application-server',
    'business-process-management',
    'container-management',
    'big-data',
    'database-as-a-service-dbaas',
    'desktop-database',
    'non-native-database-mgmt-systems',
    'nosql-databases',
    'relational-databases',
    'cloud-data-integration',
    'electronic-data-interchange-edi',
    'on-premise-data-integration',
    'data-quality',
    'data-warehouse',
    'infrastructure-as-a-service-iaas',
    'iot-management',
    'master-data-management-mdm',
    'network-monitoring',
    'operating-system',
    'other-it-infrastructure',
    'remote-desktop',
    'server-virtualization',
    'storage-management',
    'transactional-email',
    'virtual-desktop-infrastructure-vdi',
    'web-accelerator',
    'enterprise-it-management-suites',
    'it-devops-incident-management',
    'cloud-identity-and-access-management',
    'password-management',
    'sso-federation',
    'user-provisioning-governance',
    'mobile-device-management-mdm',
    'other-it-management',
    'service-desk',
    'backup',
    'data-security',
    'endpoint-protection',
    'firewall',
    'mobile-data-security',
    'network-security',
    'other-it-security',
    'virtual-private-network-vpn',
    'vulnerability-management',
    'web-security',
    'browser',
    'calendar',
    'email',
    'online-appointment-scheduling',
    'audio-editing',
    'document-creation',
    'office-suites',
    'animation',
    'other-video',
    'video-editing',
    'video-effects',
    'video-hosting',
    'diagramming',
    'other-design',
    'prototyping',
    'web-design',
    'wireframing',
    'photo-editing',
    'photo-management',
    'desktop-publishing',
    'drawing',
    'vector-graphics',
    '3d-rendering',
    '3d-painting',
    '3d-modeling',
    'other-email',
    'other-office',
    'presentation',
    'screen-and-video-capture',
    'spreadsheets',
    'survey',
    'visitor-management',
    'voice-recognition'
]

async.forEachLimit(software, 5, request_apis, write_json);

function request_apis(item, callback) {
    console.log(item)
    //request(url, scrape_apis);
    res = srequest('GET', url_base+'/categories/'+item);
    scrape_apis(null, null, res.getBody(), item);
    callback()
}

function write_json(err){
    if (err) throw err;
    console.log('\nAll requests processed!\n');
    
    fs.writeFile('apis5.json', JSON.stringify(apis, null, 4), function(err){
        console.log('APIs File successfully written!');
        console.log(apis.length);
    });
    fs.writeFile('reviews5.json', JSON.stringify(reviews, null, 4), function(err){
        console.log('Reviews File successfully written!');
        console.log(reviews.length);
    });
}

function scrape_apis(error, response, html, cat){
    if(!error){
        var $ = cheerio.load(html);
        $('div[itemprop=itemListElement]').each(function(i, elem) {
            api = $(this);
            api_stars = api.find('div.stars.margin-right-4th')
            reviews_url = api.find('h5[itemprop=name]').parent().attr('href');
            
            /*console.log(api_stars.length);
            console.log(apis_keys);
            console.log(reviews_url);*/
            
            if (api_stars.length && apis_keys.indexOf(reviews_url) < 0) {
                apis_keys.push(reviews_url)
                
                api_json = {name: '', description: '', category: cat, stars: 0, score: 0}
                api_json.name = api.find('h5[itemprop=name]').text();
                console.log('\t'+api_json.name)
                
                if ( api_stars.hasClass('stars-1') ) {
                    api_json.stars = 1;
                } else if ( api_stars.hasClass('stars-2') ) {
                    api_json.stars = 2;
                } else if ( api_stars.hasClass('stars-3') ) {
                    api_json.stars = 3;
                } else if ( api_stars.hasClass('stars-4') ) {
                    api_json.stars = 4;
                } else if ( api_stars.hasClass('stars-5') ) {
                    api_json.stars = 5;
                } else if ( api_stars.hasClass('stars-6') ) {
                    api_json.stars = 6;
                } else if ( api_stars.hasClass('stars-7') ) {
                    api_json.stars = 7;
                } else if ( api_stars.hasClass('stars-8') ) {
                    api_json.stars = 8;
                } else if ( api_stars.hasClass('stars-9') ) {
                    api_json.stars = 9;
                } else if ( api_stars.hasClass('stars-10') ) {
                    api_json.stars = 10;
                } else {
                    api_json.stars = 0;
                }
                
                api_json.score = api.find('.large-7').find('strong').text()
                
                //request(url_base+reviews_url, scrape_reviews(error, response, html, api_json));
                res = srequest('GET', url_base+reviews_url);
                scrape_reviews(null, null, res.getBody(), api_json)
                
                api_url = reviews_url.replace('reviews', 'details')
                //request(url_base+api_url, scrape_api(error, response, html, api_json));
                res = srequest('GET', url_base+api_url);
                scrape_api(null, null, res.getBody(), api_json)
                
                apis.push(api_json);
            }
        });
        /*$('h5[itemprop=name]').each(function(i, elem) {
            api_json = {name: '', description: '', category: 'Cloud Platform as a Service (PaaS)'}
            api = $(this);
            api_json.name = api.text();
            reviews_url = api.parent().attr('href');
            //request(url_base+reviews_url, scrape_reviews(error, response, html, api_json));
            res = srequest('GET', url_base+reviews_url);
            scrape_reviews(null, null, res.getBody(), api_json)
            api_url = reviews_url.replace('reviews', 'details')
            //request(url_base+api_url, scrape_api(error, response, html, api_json));
            res = srequest('GET', url_base+api_url);
            scrape_api(null, null, res.getBody(), api_json)
            apis.push(api_json);
        });*/
        
        next = $('li>a[rel=next]').last().attr('href');
        if ( next ) {
            //request(url_base+next, scrape_apis);
            res = srequest('GET', url_base+next);
            scrape_apis(null, null, res.getBody())
        }
    }
}

function scrape_api(error, response, html, json) {
    if (!error) {
        var $ = cheerio.load(html);
        json.description = $('div.paper').first().find('p').text()
    }
}

function scrape_reviews(error, response, html, json) {
    if (!error) {
        var $ = cheerio.load(html);
        $('div[itemprop=review]').each(function(i, elem) {
            review_json = {api: json.name, title: '', stars: 0, date: '', like: '', dislike: '', recommendation: '', benefit: ''}
            review = $(this);
            collect_review($, review, review_json);
            reviews.push(review_json);
        });
        next = $('li>a[rel=next]').last().attr('href');
        if ( next ) {
            //request(url_base+next, scrape_reviews, json);
            res = srequest('GET', url_base+next);
            scrape_apis(null, null, res.getBody(), json)
        }
    }
}

function collect_review($, review, json) {
    json.title = review.find('h3.review-list-heading').text();
    review_stars = review.find('div.stars');

    if ( review_stars.hasClass('stars-1') ) {
        json.stars = 1;
    } else if ( review_stars.hasClass('stars-2') ) {
        json.stars = 2;
    } else if ( review_stars.hasClass('stars-3') ) {
        json.stars = 3;
    } else if ( review_stars.hasClass('stars-4') ) {
        json.stars = 4;
    } else if ( review_stars.hasClass('stars-5') ) {
        json.stars = 5;
    } else if ( review_stars.hasClass('stars-6') ) {
        json.stars = 6;
    } else if ( review_stars.hasClass('stars-7') ) {
        json.stars = 7;
    } else if ( review_stars.hasClass('stars-8') ) {
        json.stars = 8;
    } else if ( review_stars.hasClass('stars-9') ) {
        json.stars = 9;
    } else if ( review_stars.hasClass('stars-10') ) {
        json.stars = 10;
    } else {
        json.stars = 0;
    }

    json.date = review.find('time').text();

    review.find('div[itemprop=reviewBody]').find('div').each(function(i, item) {
        if ( i == 0 ) {
            json.like = $(this).text().trim();
        } else if ( i == 1 ) {
            json.dislike = $(this).text().trim();
        } else if ( i == 2 ) {
            json.recommendation = $(this).text().trim();
        } else if ( i == 3 ) {
            json.benefit = $(this).text().trim();
        }
    })
}
