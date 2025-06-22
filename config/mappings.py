#mappings to get target msg
channel_keyword_mapping={
    'C06RC718WHX': (['threshold crossed', 'step-functions-failed', 'critical', 'not mapped on yieldcurvelookup table','[mds checker] error'], 
                    '#logs-prod', 'C082JQ9LXDK'),
    'C06QZHAHH4J': (['[mds checker] error'], '#logs-staging','C082JQ9LXDK'),
    'C07NGN4M2LF': (['error', 'failed'], '#logs-risk','C082JQ9LXDK'),
    'C08DJTQ578X': (['failed'],'#logs-pnl-runs-prod','C082JQ9LXDK')
}

channel_tag_mapping={
    's07v5f7p5nz': ('C082JQ9LXDK', '@middle-office'), 
    's07ajadld17': ('C082JQ9LXDK', '@app-support')
}

hour_action_mOCping={
    22: ['OC_VENDORF_SFTP_UPLOAD', {f'FILE_ourcompany_PROD_{get_date_range(1).strftime("%Y%m%m")}.csv'}],
    23: ['OC_VENDORK_SFTP_UPLOAD', \
            {f'ARR_TA_{get_date_range(0).strftime("%m-%d-%y") }.csv',f'TB_ALVO_{get_date_range(0).strftime("%m-%d-%y")}.csv'}],
    11: ['OC_VENDORK_SFTP_UPLOAD', \
            {f'ARR_TA_{get_date_range(0).strftime("%m-%d-%y") }.csv',f'TB_ALVO_{get_date_range(0).strftime("%m-%d-%y")}.csv'}],
}