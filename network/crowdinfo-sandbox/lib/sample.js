function validateForm(filledForm, survey) {
    var optionRange = survey.optionRange;
    var questionRange = survey.questionRange;
    console.log("optionRange");
    console.log(optionRange);
    console.log("questionRange");
    console.log(questionRange);
    console.log("filledForm");
    console.log(filledForm);
    filledForm = filledForm.replace(/'/g, '"');
    console.log(filledForm);
    filledForm = JSON.parse(filledForm);
    var questions = Object.keys(filledForm);

    if( !(questions.length==questionRange.length) ){
        return false;
    }

    for (var q in questions) {
        var question = questions[q];
        console.log("question");
        console.log(question);
        console.log("(questionRange.indexOf(question)>-1)");
        console.log((questionRange.indexOf(question)>-1));
        if( !(questionRange.indexOf(question)>-1) ){
            console.log("!(question in questionRange)");
            return false;
        }
        var option = filledForm[question];
        if( !(option==parseInt(option,10)) ) {
            return false;
        }
        if (option<1 || option>optionRange) {
            console.log("(option<1 || option>optionRange)");
            return false;
        }
    }

    return true;

    // for(var q=1; q<=questionRange; q++) {
    //     if ( !(q in filledForm && filledForm[q]<0 && filledForm[q]<=optionRange) ) {
    //         return false;
    //     }
    // }
    // return true;

    // for(var q=0; q<questions.length; q++) {
    //     console.log("Value")
    //     console.log(filledForm[questions[q]])
    //     console.log("<1")
    //     console.log(filledForm[questions[q]]<1)
    //     console.log(">optionRange")
    //     console.log(filledForm[questions[q]]>optionRange)
    //     if(filledForm[questions[q]]<1) {
    //         ret = false;
    //     }
    //     if(filledForm[questions[q]]>optionRange) {
    //         ret = false;
    //     }
    // }
    // console.log("ret");
    // console.log(ret);
    // return ret;
}

/**
 * @param {org.acme.survey.SubmitSurvey} submitSurvey
 * @transaction
 */
function onSubmitSurvey(submitSurvey) {
    if( submitSurvey.assignSurveyToken.claimed==false && validateForm(submitSurvey.filledForm, submitSurvey.assignSurveyToken.survey)
    && submitSurvey.timestamp < submitSurvey.assignSurveyToken.survey.expiryTime
    && submitSurvey.assignSurveyToken.survey.tokens>submitSurvey.assignSurveyToken.survey.payOut
    && submitSurvey.assignSurveyToken.consumer==submitSurvey.consumerAccount.consumer ) {
        console.log("Inside if block");
        submitSurvey.assignSurveyToken.survey.tokens -= submitSurvey.assignSurveyToken.survey.payOut;
        submitSurvey.consumerAccount.tokens += submitSurvey.assignSurveyToken.survey.payOut;
        submitSurvey.assignSurveyToken.claimed = true;
        return getAssetRegistry('org.acme.survey.ConsumerAccount')
               .then(function (assetRegistry) {
                   return assetRegistry.update(submitSurvey.consumerAccount);
               })
               .then(
                   getAssetRegistry('org.acme.survey.Survey')
                          .then(function (assetRegistry) {
                              return assetRegistry.update(submitSurvey.assignSurveyToken.survey);
                          })
               )
               .then(
                   getAssetRegistry('org.acme.survey.AssignSurveyToken')
                          .then(function (assetRegistry) {
                              return assetRegistry.update(submitSurvey.assignSurveyToken);
                          })
               )
    }
}

/**
 * @param {org.acme.survey.PublishSurvey} publishSurvey
 * @transaction
 */
function onPublishSurvey(publishSurvey) {
    if( publishSurvey.survey.organizationAccount==publishSurvey.organizationAccount
    && publishSurvey.organizationAccount.tokens > publishSurvey.surveyFunds ) {
        publishSurvey.organizationAccount.tokens -= publishSurvey.surveyFunds;
        publishSurvey.survey.tokens = publishSurvey.surveyFunds;
        return getAssetRegistry('org.acme.survey.OrganizationAccount')
            .then(function (assetRegistry) {
                return assetRegistry.update(publishSurvey.organizationAccount);
            })
            .then(
            getAssetRegistry('org.acme.survey.Survey')
            .then(function (assetRegistry) {
                return assetRegistry.update(publishSurvey.survey);
            })
        );
    }
}
