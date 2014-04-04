#!/usr/bin/env python
__author__ = 'abuddenberg'

from gcis_clients import WebformClient
from gcis_clients import GcisClient
from gcis_clients.sync_utils import move_images_to_gcis, sync_dataset_metadata
from collections import OrderedDict
import json
import pickle

webform = WebformClient('http://resources.assessment.globalchange.gov', 'mgTD63FAjG')

gcis_url = 'http://data.gcis-dev-front.joss.ucar.edu'
# gcis = GcisClient(gcis_url, 'andrew.buddenberg@noaa.gov', 'd9fcfd947c1785ab1cd329a9920e05e5c5d3d7f35315f164')
gcis = GcisClient('http://data-stage.globalchange.gov', 'andrew.buddenberg@noaa.gov', 'b4f1458c3cf28248c982428c46e170019327bd4c533c23dd')

sync_metadata_tree = {
    #Reports
    'nca3': OrderedDict([
        #Chapter 2
        ('our-changing-climate', [
            # (webform_url, gcis_id)
            ('/metadata/figures/2506', 'observed-change-in-very-heavy-precipitation'),
            ('/metadata/figures/2997', 'observed-change-in-very-heavy-precipitation-2'),
            ('/metadata/figures/2677', 'observed-us-precipitation-change'),
            ('/metadata/figures/3175', 'observed-us-temperature-change'),
            ('/metadata/figures/3074', 'ten-indicators-of-a-warming-world'),
            ('/metadata/figures/3170', 'global-temperature-and-carbon-dioxide'),
            ('/metadata/figures/3293', 'observed-increase-in-frostfree-season-length'),
            ('/metadata/figures/3294', 'projected-changes-in-frostfree-season-length'), #Good
            ('/metadata/figures/3305', 'variation-of-storm-frequency-and-intensity-during-the-cold-season-november--march'),
            ('/metadata/figures/2939', 'projected-changes-in-soil-moisture-for-the-western-us'),
            ('/metadata/figures/3298', 'observed-us-trend-in-heavy-precipitation'),
            ('/metadata/figures/2523', 'shells-dissolve-in-acidified-ocean-water')

        ]),
        #Chapter 4
        ('energy-supply-and-use', [
            ('/metadata/figures/3292', 'cooling-degree-days')
        ]),
        #Chapter 5
        ('transportation', [
            ('/metadata/figures/3568', 'hurricane-sandy-causes-flooding-in-new-york-city-subway-stations'),
            ('/metadata/figures/3169', 'tropical-storm-impact-on-vermont-road'),
            ('/metadata/figures/2952', 'role-of-adaptive-strategies-and-tactics-in-reducing-impacts-and-consequences')
        ]),
        #Chapter 6
        ('agriculture', [
            ('/metadata/figures/2872', 'drainage-tiles'),
            ('/metadata/figures/2691', 'projected-changes-in-key-climate-variables-affecting-agricultural-productivity')
        ]),
        #Chapter 7
        ('forests', [
            ('/metadata/figures/2977', 'effectiveness-of-forest-management-in-reducing-wildfire-risk'),
            ('/metadata/figures/2978', 'forest-vulnerability-to-changing-climate'), #Create
            ('/metadata/figures/2985', 'forests-can-be-a-source--or-a-sink--for-carbon')

        ]),
        #Chapter 8
        ('ecosystems', [
            ('/metadata/figures/2456', 'adaptation-planning-and-implementation-framework'),
            ('/metadata/figures/3574', 'biological-responses-to-climate-change')
        ]),
        #Chapter 9
        ('human-health', [
            ('/metadata/figures/2896', 'heavy-downpours-disease') #Needs images redone
        ]),
        #Chapter 10
        ('water-energy-land-use', [
            ('/metadata/figures/2410', 'coasttocoast-100degree-days-in-2011'),
            ('/metadata/figures/2986', 'hydraulic-fracturing-and-water-use'),
            ('/metadata/figures/2916', 'renewable-energy-and-land-use')
        ]),
        #Chapter 11
        ('urban-systems-infrastructure-vulnerability', [
            ('/metadata/figures/3569', 'urban-support-systems-are-interconnected')
        ]),
        #Chapter 12
        ('tribal-indigenous-native-lands-resources', [
            ('/metadata/figures/2911', 'arctic-marine-food-web')
        ]),
        #Chapter 14
        ('rural', [
            ('/metadata/figures/3306', 'growing-season-lengthens') #Needs images redone
        ]),
        # Chapter 15
        ('biogeochemical-cycles', [
            ('/metadata/figures/2575', 'many-factors-combine-to-affect-biogeochemical-cycles')
        ]),
        #Chapter 16
        ('northeast', [
            ('/metadata/figures/2995', 'projected-increases-in-the-number-of-days-over-90f'),
            ('/metadata/figures/2844', 'coney-island-after-hurricane-irene'),
            ('/metadata/figures/2846', 'storm-surge-barrier') #Wrong figurenum in GCIS
        ]),
        #Chapter 17
        ('southeast', [
            ('/metadata/figures/2998', 'projected-change-in-number-of-days-over-95-f'),
            ('/metadata/figures/2999', 'projected-change-in-number-of-nights-below-32f'),
            ('/metadata/figures/2857', 'local-planning')
        ]),
        #Chapter 18
        ('midwest', [
            ('/metadata/figures/2992', 'projected-midcentury-temperature-changes-in-the-midwest'),
            ('/metadata/figures/2994', 'when-it-rains-it-pours'),
            ('/metadata/figures/2550', 'temperatures-are-rising-in-the-midwest')
        ]),
        #Chapter 19
        ('great-plains', [
            ('/metadata/figures/2697', 'temperature-and-precipitation-distribution-in-the-great-plains'), #Needs images redone
            ('/metadata/figures/2989', 'projected-change-in-number-of-hot-days'),
            ('/metadata/figures/2991', 'projected-change-in-number-of-heavy-precipitation-days'),
            ('/metadata/figures/3002', 'projected-change-in-number-of-consecutive-dry-days'),
            ('/metadata/figures/2990', 'projected-change-in-number-of-warm-nights')
        ]),
        #Chapter 25
        ('coastal-zone', [
            ('/metadata/figures/2543', 'coastal-ecosystem-services')
        ]),
        # Climate Science Appendix
        ('appendix-climate-science', [
            ('/metadata/figures/3147', 'ice-loss-from-greenland-and-antarctica')
        ])
    ])
}


def main():
    # print gcis.test_login()
    # sync_dataset_metadata(aggregate_webform_datasets())
    sync(replace=True)

    # f = webform.get_webform('/metadata/figures/2575', download_images=True)
    # print gcis.create_figure('nca3', 'biogeochemical-cycles', f)


def sync(replace=False):
    for report_id in sync_metadata_tree:
        for chapter_id in sync_metadata_tree[report_id]:
            for figure_ids in sync_metadata_tree[report_id][chapter_id]:
                webform_url, gcis_id = figure_ids

                print 'Attempting to sync: {id}'.format(id=gcis_id)

                #Merge data from both systems into one object...
                figure_obj = webform.get_webform(webform_url).merge(
                    gcis.get_figure(report_id, gcis_id, chapter_id=chapter_id)
                )

                if replace:
                    for image in figure_obj.images:
                        #TODO: There are better ways to do this. Build File support.
                        print 'Deleting {img}'.format(img=image.identifier)
                        gcis.delete_image(image)

                    print 'Attempting to upload: {id}'.format(id=gcis_id)
                    move_images_to_gcis(webform, gcis, webform_url, gcis_id, report_id)

                #...then send it.
                gcis.update_figure(report_id, chapter_id, figure_obj)

                print 'Success!'

if __name__ == '__main__':
    main()