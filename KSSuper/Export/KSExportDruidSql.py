from  BatchSql.KSBatchSql import KSBatchSql
class KSExportDruidSql(object):
    # !/usr/bin/env python
    # coding: utf-8

    # 公共字段
    public_fields = "'job_title','name','source','source_type','hire_mode','opened_at','tags','city','is_intern',"
    public_fields_select = '''
      IFNULL(cd.job_title,'') AS job_title,
      IFNULL(cd.`name`,'') AS `name`,
      IFNULL(cd.source,'') AS source,
      IFNULL(cd.source_type,'') AS source_type,
      IF(IFNULL(cd.hire_mode,'')='', '未知',cd.hire_mode) as hire_mode,
      IFNULL(j.opened_at,'未知') AS `opened_at`,
      IFNULL(j.tags,'') AS tags,
      IFNULL(j.city,IF(cd.job_title REGEXP '广州','广州市',IF(cd.job_title REGEXP '上海','上海市',IF(cd.job_title REGEXP '青岛',
            '青岛市',IF(cd.job_title REGEXP 'SH','上海市',IF(cd.job_title REGEXP 'GZ','广州市',IF(cd.job_title REGEXP 'QD','青岛市',
            '青岛市'))))))) AS city,
      IFNULL(cd.is_intern,'未知') AS is_intern,'''

    public_tables = '''candidates cd
      left join 
              (select j.id,j.moka_job_id,j.title,j.opened_at,jl.city,j.tags
              from jobs as j
              left join job_locations as jl on j.id = jl.job_id
              ) as  j on j.moka_job_id = cd.moka_job_id'''

    public_wheres = "1 group by cd.id"

    # 简历
    full_sql_resume = '''
      SELECT ''' + public_fields_select + '''
      IFNULL(cd.add_time,'') AS` timestamp`,
      '是' AS receive_resume
      FROM ''' + public_tables + '''
      WHERE cd.add_time IS NOT NULL AND ''' + public_wheres + ';'

    # 初筛
    full_sql_filter1 = '''
      SELECT ''' + public_fields_select + '''
      IFNULL(ol.created_at,'') AS` timestamp`,
      IFNULL(ol.frist_filter_status,'') AS frist_filter_status
      FROM ''' + public_tables + '''
      inner join
              (
              SELECT ol.application_id,max(ol.created_at) as created_at,IF(ol.type='10','通过','未通过') as frist_filter_status FROM operation_logs as ol 
              where (ol.stage_id='13395' and type='10') or (ol.stage_id='13394' and type='4') 
              GROUP BY ol.application_id
              ) as ol on ol.application_id=cd.application_id
      WHERE ol.frist_filter_status IS NOT NULL AND ''' + public_wheres + ';'

    # 部门筛选
    full_sql_filter2 = '''
      SELECT ''' + public_fields_select + '''
      IFNULL(ol.created_at,'') AS` timestamp`,
      IFNULL(ol.department_filter_status,'') AS department_filter_status
      FROM ''' + public_tables + '''
      inner join
              (
              SELECT ol.application_id,max(ol.created_at) as created_at,IF(ol.type='10','通过','未通过') as department_filter_status FROM operation_logs as ol 
              where (ol.stage_id='13396' and type='10') or (ol.stage_id='13395' and type='4') 
              GROUP BY ol.application_id
              ) as ol on ol.application_id=cd.application_id
      WHERE ol.department_filter_status IS NOT NULL AND ''' + public_wheres + ';'

    # 初试
    full_sql_interview1 = '''
      SELECT ''' + public_fields_select + '''
      IFNULL(it.add_time,'') AS` timestamp`,
      IFNULL(it.interview_status,'') AS interview_status
      FROM ''' + public_tables + '''
      inner join
              (
              select c.id, c.name, IF(min(i.result_type)=1,'通过','未通过')as interview_status,i.add_time 
              from candidates as c 
              left join interviews as i on c.id = i.candidate_id 
              where i.round_name = '初试' group by c.id,i.add_time
              ) as it ON it.id=cd.id
      WHERE it.interview_status IS NOT NULL AND ''' + public_wheres + ';'

    # 复试
    full_sql_interview2 = '''
      SELECT ''' + public_fields_select + '''
      IFNULL(it.add_time,'') AS` timestamp`,
      IFNULL(it.interview_2_status,'') AS interview_2_status
      FROM ''' + public_tables + '''
      inner join
              (
              select c.id, c.name, IF(min(i.result_type)=1,'通过','未通过')as interview_2_status,i.add_time 
              from candidates as c 
              left join interviews as i on c.id = i.candidate_id 
              where i.round_name = '复试' group by c.id,i.add_time
              ) as it ON it.id=cd.id
      WHERE it.interview_2_status IS NOT NULL AND ''' + public_wheres + ';'

    # offer申请
    full_sql_offer_application = '''
      SELECT ''' + public_fields_select + '''
      IFNULL(offer.`offer_application_end_at`,'') AS `timestamp`,
      '是' as offer_application
      FROM ''' + public_tables + '''
      inner join offer_table_datas as offer on offer.`name` = cd.`name`
      WHERE offer.`offer_application_end_at` IS NOT NULL AND ''' + public_wheres + ';'

    # offer审核
    full_sql_offer_reply = '''
      SELECT ''' + public_fields_select + '''
      IFNULL(offer.`offer_reply_end_at`,'') AS `timestamp`,
      IFNULL(offer.offer_reply_status,'未通过') AS `offer_reply_status`
      FROM ''' + public_tables + '''
      inner join offer_table_datas as offer on offer.`name` = cd.`name`
      WHERE offer.offer_reply_end_at IS NOT NULL AND ''' + public_wheres + ';'

    # offer发送
    full_sql_offer_send = '''
      SELECT ''' + public_fields_select + '''
      offer.`offer_send_end_at` as timestamp , 
      '是' as offer_send
      FROM ''' + public_tables + '''
      inner join offer_table_datas as offer on offer.`name` = cd.`name`
      WHERE offer.offer_send_end_at IS NOT NULL AND ''' + public_wheres + ';'

    # 入职
    full_sql_entry = '''
      SELECT ''' + public_fields_select + '''
      IFNULL(offer.`entry_end_at`,'') AS `timestamp`,
      '是' as entry
      FROM ''' + public_tables + '''
      inner join offer_table_datas as offer on offer.`name` = cd.`name`
      WHERE offer.entry_end_at IS NOT NULL AND ''' + public_wheres + ';'

    # full_sql = full_sql_resume \
    #            + full_sql_filter1 \
    #            + full_sql_filter2 \
    #            + full_sql_interview1 \
    #            + full_sql_interview2 \
    #            + full_sql_offer_application \
    #            + full_sql_offer_reply \
    #            + full_sql_offer_send \
    #            + full_sql_entry
    # print(full_sql)

    druid_sqls = [full_sql_resume,
                  full_sql_filter1,
                  full_sql_filter2,
                  full_sql_interview1,
                  full_sql_interview2,
                  full_sql_offer_application,
                  full_sql_offer_reply,
                  full_sql_offer_send,
                  full_sql_entry]

    # bat = KSBatchSql()
    # out_path = "/Users/saeipi/Desktop/jobs"
    # index = 0
    # for sql in druid_sqls:
    #     bat.execute_select_sql(sql,out_path,str(index)+"_data")
    #     index = index + 1

